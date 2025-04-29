from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph
from google_a2a.common.types import Task
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from google_a2a.common.types import Message
from langchain_core.tools import BaseTool
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient


@asynccontextmanager
async def get_tools(config):
    async with MultiServerMCPClient(config) as client:
        print("Tools: ", client.get_tools())
        yield client.get_tools()


def create_agent(prompt: str = None, tools: list[BaseTool] = None):
    anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.2)
    agent = create_react_agent(anthropic_llm, prompt=prompt, tools=tools)
    return agent


def langchain_message_to_a2a_message(message: AIMessageChunk | AIMessage) -> Message:
    content = message.content
    parts = []

    def tool_call_to_a2a_message_part(tool_call: dict) -> Message:
        return {
            "type": "text",
            "text": f"Using tool: {tool_call['name']} with args: {tool_call['args']}",
        }

    def tool_use_to_a2a_message_part(tool_use: dict) -> Message:
        return {
            "type": "text",
            "text": tool_use["partial_json"],
        }

    if isinstance(content, str):
        parts.append({"type": "text", "text": content})
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, str):
                parts.append({"type": "text", "text": item})
            elif isinstance(item, dict):
                if item["type"] == "tool_call":
                    parts.append(tool_call_to_a2a_message_part(item))
                elif (
                    item["type"] == "tool_use" and item.get("partial_json") is not None
                ):
                    parts.append(tool_use_to_a2a_message_part(item))
                elif item["type"] == "text":
                    parts.append({"type": "text", "text": item["text"]})
                else:
                    print(f"Unknown item type: {type(item)}, item: {item}")
            else:
                print(f"Unknown item type: {type(item), item: {item}}")

    return Message(role="agent", parts=parts)


def a2a_message_to_langchain_message(message: Message) -> HumanMessage | AIMessage:
    try:
        if message.role == "user":
            return HumanMessage(
                content=[{"type": "text", "text": part.text} for part in message.parts]
            )
        else:
            return AIMessage(
                content=[{"type": "text", "text": part.text} for part in message.parts]
            )
    except Exception as e:
        print(f"Error converting A2A message to Langchain message: {e}")
        return None


async def run_agent_stream(agent: CompiledGraph, task: Task):
    messages = [a2a_message_to_langchain_message(message) for message in task.history]
    async for chunk in agent.astream({"messages": messages}, stream_mode="messages"):
        yield chunk


async def run_agent(agent: CompiledGraph, task: Task):
    messages = [a2a_message_to_langchain_message(message) for message in task.history]
    return await agent.ainvoke({"messages": messages})
