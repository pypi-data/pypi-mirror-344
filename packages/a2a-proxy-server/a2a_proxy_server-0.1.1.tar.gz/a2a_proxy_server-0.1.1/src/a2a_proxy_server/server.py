from starlette.applications import Starlette
from starlette.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request
from google_a2a.common.types import (
    A2ARequest,
    JSONRPCResponse,
    InvalidRequestError,
    JSONParseError,
    GetTaskRequest,
    CancelTaskRequest,
    SendTaskRequest,
    SetTaskPushNotificationRequest,
    GetTaskPushNotificationRequest,
    InternalError,
    AgentCard,
    TaskResubscriptionRequest,
    SendTaskStreamingRequest,
)
from pydantic import ValidationError
import json
from typing import AsyncIterable, Any
from google_a2a.common.server.task_manager import TaskManager

import logging

logger = logging.getLogger(__name__)


class A2AProxyServer:
    def __init__(
        self,
        host="0.0.0.0",
        port=5000,
    ):
        self.host = host
        self.port = port
        self.task_managers = {}
        self.agent_cards = {}
        self.app = Starlette()
        self.app.add_route("/{agent_id}", self._process_request, methods=["POST"])
        self.app.add_route(
            "/{agent_id}/.well-known/agent.json", self._get_agent_card, methods=["GET"]
        )

    def register_agent(
        self, agent_id: str, agent_card: AgentCard, task_manager: TaskManager
    ):
        self.agent_cards[agent_id] = agent_card
        self.task_managers[agent_id] = task_manager

    def start(self):
        import uvicorn

        uvicorn.run(self.app, host=self.host, port=self.port)

    def _get_agent_card(self, request: Request) -> JSONResponse:
        agent_id = request.path_params.get("agent_id")
        agent_card = self.agent_cards.get(agent_id)
        if not agent_card:
            raise ValueError(f"Agent {agent_id} not found")
        return JSONResponse(agent_card.model_dump(exclude_none=True))

    async def _process_request(self, request: Request):
        agent_id = request.path_params.get("agent_id")
        logger.info(f"Processing request for agent {agent_id}")
        task_manager = self.task_managers.get(agent_id)
        if task_manager is None:
            raise ValueError(f"Agent {agent_id} not found")

        try:
            body = await request.json()
            json_rpc_request = A2ARequest.validate_python(body)

            if isinstance(json_rpc_request, GetTaskRequest):
                result = await task_manager.on_get_task(json_rpc_request)
            elif isinstance(json_rpc_request, SendTaskRequest):
                result = await task_manager.on_send_task(json_rpc_request)
            elif isinstance(json_rpc_request, SendTaskStreamingRequest):
                result = await task_manager.on_send_task_subscribe(json_rpc_request)
            elif isinstance(json_rpc_request, CancelTaskRequest):
                result = await task_manager.on_cancel_task(json_rpc_request)
            elif isinstance(json_rpc_request, SetTaskPushNotificationRequest):
                result = await task_manager.on_set_task_push_notification(
                    json_rpc_request
                )
            elif isinstance(json_rpc_request, GetTaskPushNotificationRequest):
                result = await task_manager.on_get_task_push_notification(
                    json_rpc_request
                )
            elif isinstance(json_rpc_request, TaskResubscriptionRequest):
                result = await task_manager.on_resubscribe_to_task(json_rpc_request)
            else:
                logger.warning(f"Unexpected request type: {type(json_rpc_request)}")
                raise ValueError(f"Unexpected request type: {type(request)}")

            return self._create_response(result)

        except Exception as e:
            return self._handle_exception(e)

    def _handle_exception(self, e: Exception) -> JSONResponse:
        if isinstance(e, json.decoder.JSONDecodeError):
            json_rpc_error = JSONParseError()
        elif isinstance(e, ValidationError):
            json_rpc_error = InvalidRequestError(data=json.loads(e.json()))
        else:
            logger.error(f"Unhandled exception: {e}")
            json_rpc_error = InternalError()

        response = JSONRPCResponse(id=None, error=json_rpc_error)
        return JSONResponse(response.model_dump(exclude_none=True), status_code=400)

    def _create_response(self, result: Any) -> JSONResponse | EventSourceResponse:
        if isinstance(result, AsyncIterable):

            async def event_generator(result) -> AsyncIterable[dict[str, str]]:
                async for item in result:
                    yield {"data": item.model_dump_json(exclude_none=True)}

            return EventSourceResponse(event_generator(result))
        elif isinstance(result, JSONRPCResponse):
            return JSONResponse(result.model_dump(exclude_none=True))
        else:
            logger.error(f"Unexpected result type: {type(result)}")
            raise ValueError(f"Unexpected result type: {type(result)}")
