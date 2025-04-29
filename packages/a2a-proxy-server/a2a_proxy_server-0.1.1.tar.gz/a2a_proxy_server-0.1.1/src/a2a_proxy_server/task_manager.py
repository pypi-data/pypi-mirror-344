from typing import AsyncIterable
import asyncio

from google_a2a.common.server.task_manager import InMemoryTaskManager
from google_a2a.common.types import (
    Artifact,
    JSONRPCResponse,
    Message,
    SendTaskRequest,
    SendTaskResponse,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
    Task,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)
from a2a_proxy_server.agent import (
    run_agent_stream,
    run_agent,
    create_agent,
    langchain_message_to_a2a_message,
    get_tools,
)


class AgentTaskManager(InMemoryTaskManager):
    def __init__(self, tool_config=None, prompt=None):
        super().__init__()
        self.agent = None
        self.tool_config = tool_config
        self.agent_context = None
        self.prompt = prompt

    async def initialize_agent(self):
        tools = []
        if self.tool_config:
            self.agent_context = get_tools(self.tool_config)
            tools = await self.agent_context.__aenter__()
        print("Tools: ", tools)
        self.agent = create_agent(prompt=self.prompt, tools=tools)

    async def shutdown(self):
        if self.agent_context:
            await self.agent_context.__aexit__(None, None, None)

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        # Ensure agent is initialized
        if not self.agent:
            await self.initialize_agent()

        # Upsert a task stored by InMemoryTaskManager
        await self.upsert_task(request.params)
        task_id = request.params.id
        task = self.tasks[task_id]
        response = await run_agent(self.agent, task)
        messages = response.get("messages", [])
        task = await self._update_task(
            task_id=task_id,
            task_state=TaskState.COMPLETED,
            ai_message=langchain_message_to_a2a_message(messages[-1]),
        )

        # Send the response
        return SendTaskResponse(id=request.id, result=task)

    async def _update_task(
        self,
        task_id: str,
        task_state: TaskState,
        ai_message: Message,
    ) -> Task:
        task = self.tasks[task_id]
        task.status = TaskStatus(
            state=task_state,
            message=ai_message,
        )
        task.artifacts = [
            Artifact(
                parts=ai_message.parts,
            )
        ]
        task.history.append(ai_message)
        return task

    async def _process_task(self, task: Task):
        async for chunk, _ in run_agent_stream(self.agent, task):
            ai_message = langchain_message_to_a2a_message(chunk)
            task_update_event = TaskStatusUpdateEvent(
                id=task.id,
                status=TaskStatus(state=TaskState.WORKING, message=ai_message),
                final=False,
            )
            await self.enqueue_events_for_sse(task.id, task_update_event)

        task_complete_event = TaskStatusUpdateEvent(
            id=task.id,
            status=TaskStatus(state=TaskState.COMPLETED),
            final=True,
        )
        await self.enqueue_events_for_sse(task.id, task_complete_event)

    async def on_send_task_subscribe(
        self, request: SendTaskStreamingRequest
    ) -> AsyncIterable[SendTaskStreamingResponse] | JSONRPCResponse:
        # Ensure agent is initialized
        if not self.agent:
            await self.initialize_agent()

        # Upsert a task stored by InMemoryTaskManager
        await self.upsert_task(request.params)

        task_id = request.params.id
        task = self.tasks[task_id]

        # Create a queue of work to be done for this task
        sse_event_queue = await self.setup_sse_consumer(task_id=task_id)

        # Start the asynchronous work for this task
        asyncio.create_task(self._process_task(task))

        # Tell the client to expect future streaming responses
        return self.dequeue_events_for_sse(
            request_id=request.id,
            task_id=task_id,
            sse_event_queue=sse_event_queue,
        )
