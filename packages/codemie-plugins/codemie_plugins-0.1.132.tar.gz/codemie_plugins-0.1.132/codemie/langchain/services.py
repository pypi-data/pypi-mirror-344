# pylint: disable=no-member
import asyncio
import json
import os
from typing import Optional, Callable

import nats
import uuid
from langchain.tools import BaseTool
from langchain_core.messages import ToolMessage

import codemie.generated.proto.v1.service_pb2 as service_pb2
from codemie.logging import logger


class ToolService:
    """Concrete ToolGate service tool implementation."""

    def __init__(self,
        nats_config: dict,
        tool: BaseTool,
        timeout: int,
        prefix: str = None,
        tool_result_converter: Optional[Callable[[ToolMessage], str]] = None
    ):
        self.nats_config = nats_config
        self.tool = tool
        self.prefix = prefix
        self.nc = None
        self.subject = prefix + "." + tool.name
        self.plugin_key = prefix.split(".")[0]
        self.timeout = timeout
        self._running = False
        self._task = None
        self.tool_result_converter = tool_result_converter
        self.nats_max_payload = os.environ.get("NATS_MAX_PAYLOAD", None)


    def serve(self):
        """
        Start serving in the current thread by running the event loop.
        This should only be called if there's no event loop running.
        """
        try:
            asyncio.run(self.a_serve())
        except RuntimeError as e:
            if "already running" in str(e):
                logger.warning("Event loop is already running. Use start() instead of serve().")
                raise RuntimeError("Cannot call serve() from an async context. Use start() instead.")
            raise

    async def start(self):
        """
        Start the service asynchronously and return immediately.
        This should be used when there's already an event loop running.
        """
        if self._task is not None and not self._task.done():
            logger.warning("Service is already running")
            return

        self._running = True
        self._task = asyncio.create_task(self.a_serve())
        return self._task

    async def stop(self):
        """Stop the service gracefully."""
        self._running = False
        if self.nc:
            await self.nc.drain()
            self.nc = None
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def a_serve(self):
        """Serve the tool by subscribing to the NATS server."""
        try:
            self.nc = await nats.connect(
                servers=self.nats_config["servers"],
                **self.nats_config["options"],
                error_cb=self._on_error,
                disconnected_cb=self._on_disconnect,
                reconnected_cb=self._on_reconnect,
                closed_cb=self._on_close
            )
            if self.nats_max_payload:
                logger.info(f"Setting NATS max payload to {self.nats_max_payload} bytes for tool {self.tool.name}")
                self.nc._max_payload = int(self.nats_max_payload)
            await self.subscribe()

            # Replace the infinite loop with a more controlled approach
            while self._running:
                try:
                    await asyncio.sleep(1)
                except asyncio.CancelledError:
                    logger.info(f"Service for tool {self.tool.name} was cancelled")
                    break

        except Exception as e:
            logger.error(f"Error in a_serve for {self.tool.name}: {str(e)}")
            self._running = False
            raise
        finally:
            if self.nc:
                await self.nc.drain()
                self.nc = None

        # Add callback handlers for NATS connection events
    async def _on_error(self, e):
        logger.error(f"NATS error for tool {self.tool.name}: {str(e)}")

    async def _on_disconnect(self):
        logger.warning(f"NATS disconnected for tool {self.tool.name}")

    async def _on_reconnect(self):
        logger.info(f"NATS reconnected for tool {self.tool.name}")

    async def _on_close(self):
        logger.info(f"NATS connection closed for tool {self.tool.name}")
        self._running = False

    async def execute_tool_with_timeout(self, query, timeout):
        error_message = "Call to the tool timed out."
        try:
            tool_input = json.loads(query)
            logger.info("Running tool %s with input: %s", self.tool.name, tool_input)
            tool_response = await asyncio.wait_for(
                self.tool.arun(tool_input, tool_call_id=str(uuid.uuid4())), timeout
            )
            logger.info("Tool %s returned:\n%s\n", self.tool.name, tool_response)
            return tool_response

        except asyncio.TimeoutError:
            logger.error("The operation timed out.")
            return error_message
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON.")
            return "Failed to decode JSON."
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return f"An error occurred: {e}"

    async def subscribe(self):
        """Subscribe to the service subject and run handlers."""

        async def _info_handler(msg):
            logger.debug("Running tool handler %s", self.tool.name)
            response = service_pb2.ServiceResponse()
            response.meta.subject = self.subject
            response.meta.handler = service_pb2.Handler.GET
            response.meta.puppet = service_pb2.Puppet.LANGCHAIN_TOOL
            response.puppet_response.lc_tool.name = self.tool.name
            response.puppet_response.lc_tool.description = self.tool.description
            # Handle both dict and BaseModel cases
            if hasattr(self.tool.args_schema, 'model_json_schema'):
                args_schema_json = json.dumps(self.tool.args_schema.model_json_schema())
            elif isinstance(self.tool.args_schema, dict):
                args_schema_json = json.dumps(self.tool.args_schema)
            else:
                args_schema_json = None
            response.puppet_response.lc_tool.args_schema = args_schema_json
            await self.nc.publish(msg.reply, response.SerializeToString())

        async def _run_handler(msg, query: str = None):
            logger.info("Running tool %s with query: %s", self.tool.name, query)
            response = service_pb2.ServiceResponse()
            response.meta.subject = self.subject
            response.meta.handler = service_pb2.Handler.RUN
            response.meta.puppet = service_pb2.Puppet.LANGCHAIN_TOOL
            try:
                tool_response = await self.execute_tool_with_timeout(query, self.timeout)
                converted_response = (
                    self.tool_result_converter(tool_response) if self.tool_result_converter else str(tool_response)
                )
                response.puppet_response.lc_tool.result = converted_response

            except Exception as exc:
                error_message = f"Tool {self.tool.name} got error: {exc}"
                logger.error(error_message, exc_info=True)
                response.puppet_response.lc_tool.error = error_message

            await self.nc.publish(msg.reply, response.SerializeToString())
        
        async def _subject_discovery_handler(msg):
            await self.nc.publish(msg.reply, self.subject.encode())

        async def _main_handler(msg):
            logger.debug("Running main handler for message: %s", msg.data)
            request = service_pb2.ServiceRequest()
            request.ParseFromString(msg.data)
            if request.IsInitialized():
                if (
                    request.meta.subject == self.subject
                    and request.meta.handler == service_pb2.Handler.GET
                    and request.meta.puppet == service_pb2.Puppet.LANGCHAIN_TOOL
                ):
                    await _info_handler(msg)
                elif (
                    request.meta.subject == self.subject
                    and request.meta.handler == service_pb2.Handler.RUN
                    and request.meta.puppet == service_pb2.Puppet.LANGCHAIN_TOOL
                ):
                    await _run_handler(msg, query=request.puppet_request.lc_tool.query)

        sub = await self.nc.subscribe(self.subject, cb=_main_handler)
        await self.nc.subscribe(self.plugin_key + "." + "ping", cb=_subject_discovery_handler)

        if sub:
            parts = sub.subject.split('.')
            logger.info("Tool %s got subscribed to %s", self.tool.name, '$PLUGIN_KEY.'+'.'.join(parts[1:]))
        while True:
            await asyncio.sleep(1)

    def tool_metadata_dict(self):
        """Return a dictionary representation of the tool metadata."""

        return {
            "name": self.tool.name,
            "description": self.tool.description,
            "args_schema": (
                self.tool.args_schema.schema() if self.tool.args_schema else None
            ),
        }
