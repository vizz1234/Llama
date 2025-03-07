import os
import nest_asyncio
import llama_index.core
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.tools import QueryEngineTool
from typing import Dict, List, Any, Optional
from llama_index.core.llms import ChatMessage
from llama_index.core.llms.llm import ToolSelection, LLM
from llama_index.core.workflow import (
    Workflow,
    Event,
    StartEvent,
    StopEvent,
    step,
    Context,
)
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import BaseTool
from llama_index.utils.workflow import draw_all_possible_flows
from IPython.display import display, Markdown
import asyncio
import streamlit as st

# Initialize OpenAI and Phoenix settings
os.environ["OPENAI_API_KEY"] = st.secrets["api_keys"]["OPENAI_API_KEY"]
PHOENIX_API_KEY = st.secrets["api_keys"]["PHOENIX_API_KEY"]
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
llama_index.core.set_global_handler("arize_phoenix", endpoint="https://llamatrace.com/v1/traces")
Settings.llm = OpenAI("gpt-3.5-turbo")

# Create LlamaCloud index
index = LlamaCloudIndex(
    name=st.secrets["llama_cloud"]["INDEX_NAME"],
    project_name=st.secrets["llama_cloud"]["PROJECT_NAME"],
    organization_id=st.secrets["api_keys"]["ORGANIZATION_ID"],
    api_key=st.secrets["api_keys"]["LLAMA_CLOUD_API_KEY"]
)

llama_cloud_query_engine = index.as_query_engine()

# Create LlamaCloud tool
llama_cloud_tool = QueryEngineTool.from_defaults(
    query_engine=llama_cloud_query_engine,
    description="Useful for answering semantic questions about certain cities in the US.",
    name="llama_cloud_tool"
)

def create_llama_tool(index):
    """Create a LlamaIndex query tool from an index."""
    query_engine = index.as_query_engine()
    return QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description="Useful for querying information from uploaded documents.",
        name="llama_tool"
    )

class InputEvent(Event):
    """Input event."""

class GatherToolsEvent(Event):
    """Gather Tools Event"""

    tool_calls: Any

class ToolCallEvent(Event):
    """Tool Call event"""

    tool_call: ToolSelection

class ToolCallEventResult(Event):
    """Tool call event result."""

    msg: ChatMessage

class RouterOutputAgentWorkflow(Workflow):
    """Custom router output agent workflow."""

    def __init__(self,
        tools: List[BaseTool],
        timeout: Optional[float] = 10.0,
        disable_validation: bool = False,
        verbose: bool = False,
        llm: Optional[LLM] = None,
        chat_history: Optional[List[ChatMessage]] = None,
    ):
        """Constructor."""

        super().__init__(timeout=timeout, disable_validation=disable_validation, verbose=verbose)

        self.tools: List[BaseTool] = tools
        self.tools_dict: Optional[Dict[str, BaseTool]] = {tool.metadata.name: tool for tool in self.tools}
        self.llm: LLM = llm or OpenAI(temperature=0, model="gpt-3.5-turbo")
        self.chat_history: List[ChatMessage] = chat_history or []


    def reset(self) -> None:
        """Resets Chat History"""

        self.chat_history = []

    @step()
    async def prepare_chat(self, ev: StartEvent) -> InputEvent:
        message = ev.get("message")
        if message is None:
            raise ValueError("'message' field is required.")

        # add msg to chat history
        chat_history = self.chat_history
        chat_history.append(ChatMessage(role="user", content=message))
        return InputEvent()

    @step()
    async def chat(self, ev: InputEvent) -> GatherToolsEvent | StopEvent:
        """Appends msg to chat history, then gets tool calls."""

        # Put msg into LLM with tools included
        chat_res = await self.llm.achat_with_tools(
            self.tools,
            chat_history=self.chat_history,
            verbose=self._verbose,
            allow_parallel_tool_calls=True
        )
        tool_calls = self.llm.get_tool_calls_from_response(chat_res, error_on_no_tool_call=False)

        ai_message = chat_res.message
        self.chat_history.append(ai_message)
        if self._verbose:
            print(f"Chat message: {ai_message.content}")

        # no tool calls, return chat message.
        if not tool_calls:
            return StopEvent(result=ai_message.content)

        return GatherToolsEvent(tool_calls=tool_calls)

    @step(pass_context=True)
    async def dispatch_calls(self, ctx: Context, ev: GatherToolsEvent) -> ToolCallEvent:
        """Dispatches calls."""

        tool_calls = ev.tool_calls
        await ctx.set("num_tool_calls", len(tool_calls))

        # trigger tool call events
        for tool_call in tool_calls:
            ctx.send_event(ToolCallEvent(tool_call=tool_call))

        return None

    @step()
    async def call_tool(self, ev: ToolCallEvent) -> ToolCallEventResult:
        """Calls tool."""

        tool_call = ev.tool_call

        # get tool ID and function call
        id_ = tool_call.tool_id

        if self._verbose:
            print(f"Calling function {tool_call.tool_name} with msg {tool_call.tool_kwargs}")

        # call function and put result into a chat message
        tool = self.tools_dict[tool_call.tool_name]
        output = await tool.acall(**tool_call.tool_kwargs)
        msg = ChatMessage(
            name=tool_call.tool_name,
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": tool_call.tool_name
            }
        )

        return ToolCallEventResult(msg=msg)

    @step(pass_context=True)
    async def gather(self, ctx: Context, ev: ToolCallEventResult) -> StopEvent | None:
        """Gathers tool calls."""
        # wait for all tool call events to finish.
        tool_events = ctx.collect_events(ev, [ToolCallEventResult] * await ctx.get("num_tool_calls"))
        if not tool_events:
            return None

        for tool_event in tool_events:
            # append tool call chat messages to history
            self.chat_history.append(tool_event.msg)

        # # after all tool calls finish, pass input event back, restart agent loop
        return InputEvent()

async def main():
    wf = RouterOutputAgentWorkflow(tools=[sql_tool, llama_cloud_tool], verbose=True, timeout=120)
    draw_all_possible_flows(RouterOutputAgentWorkflow)
    queries = ["Which city has the highest population?", "List all places to visit in Miami.", "How do people in Chicago get around?", "What is the historical name of Los Angeles?"]
    for query in queries:
        result = await wf.run(message=query)
        display(Markdown(result))

if __name__ == "__main__":
    asyncio.run(main())