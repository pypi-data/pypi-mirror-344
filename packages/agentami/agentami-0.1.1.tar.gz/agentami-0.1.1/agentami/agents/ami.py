from typing import List, Optional, Callable, Set, Dict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import ToolMessage, SystemMessage, BaseMessage
from langchain_core.tools import Tool
from langgraph.graph import StateGraph, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.base import BaseCheckpointSaver
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from agentami.tool_selector.tool_selector import ToolRetriever
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class State(TypedDict):
    """State representing the agent's context, including messages and selected tools."""
    messages: Annotated[List[BaseMessage], add_messages]
    selected_tools: Set[str]


class AgentAmi:
    """A class that represents the Agent Ami responsible for interacting with tools and LLMs."""

    def __init__(
            self,
            *,
            model: BaseChatModel,
            tools: Optional[List[Tool]] = None,
            checkpointer: Optional[BaseCheckpointSaver] = None,
            tool_selector: Optional[Callable[[str, int], List[str]]] = None,
            top_k: int = 7,
            context_size: Optional[int] = None,
            disable_pruner: Optional[bool] = False,
            prompt_template: Optional[str] = "You are a helpful assistant. Use tools if necessary."
    ):
        """
        Initializes the AgentAmi instance.

        Args:
            model (BaseChatModel): The LLM model to be used.
            tools (Optional[List[Tool]]): A list of tools that the agent can use.
            checkpointer (Optional[BaseCheckpointSaver]): An optional checkpoint saver.
            tool_selector (Optional[Callable]): A function to select relevant tools based on the user's input.
            top_k (int): The number of tools to select based on relevance. Defaults to 7.
            context_size (Optional[int]): The maximum number of messages to retain in context.
            disable_pruner (Optional[bool]): Whether to disable the pruner for tool selection. Defaults to False.
            prompt_template (Optional[str]): The template to use for the LLM prompt.
        """
        self._validate_init_args(model, tools, checkpointer, tool_selector, top_k, context_size, disable_pruner,
                                 prompt_template)
        self.llm = model
        self.tools = tools or []
        self.checkpointer = checkpointer
        self.top_k = top_k
        self.context_size = context_size
        self.tool_registry = {tool.name: tool for tool in self.tools}
        self.disable_pruner = disable_pruner
        self.graph = self._build_agent()
        self.prompt_template = prompt_template
        if not tool_selector:
            self._toolkit_retriever = ToolRetriever(tools=self.tools)
            self.tool_selector = self._toolkit_retriever.get_relevant_tools_only
        else:
            self.tool_selector = tool_selector

    def _agent_node(self) -> Callable[[State], Dict[str, List[BaseMessage]]]:
        """
        Returns a LangGraph node that handles the agent's response generation using the LLM and selected tools.

        Returns:
            Callable: A function that takes the state and returns the agent's response.
        """

        def _node(state: State) -> Dict[str, List[BaseMessage]]:
            selected_tools = [self.tool_registry[tool_id] for tool_id in state["selected_tools"]]
            llm_with_tools = self.llm.bind_tools(selected_tools)
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=self.prompt_template),
                MessagesPlaceholder(variable_name="messages")  # Use actual conversation history
            ])
            formatted_messages = prompt.format_messages(messages=state["messages"])
            response = {"messages": [llm_with_tools.invoke(formatted_messages)]}
            return response

        return _node

    def _select_relevant_tools_node(self) -> Callable[[State], Dict[str, Set[str]]]:
        """
        Returns a LangGraph node that selects relevant tools based on the latest message in the state.

        Returns:
            Callable: A function that selects relevant tools for the agent based on the current state.
        """

        def _node(state: State) -> Dict[str, Set[str]]:
            self._state_pruner(state)
            last_message = state["messages"][-1]
            relevant_tools = self.tool_selector(last_message.content, self.top_k)
            new_tool_set = state.get('selected_tools', set())
            new_tool_set.update(relevant_tools)
            return {"selected_tools": new_tool_set}

        return _node

    def _build_agent(self) -> CompiledStateGraph:
        """
        Builds and compiles the LangGraph agent, including the nodes for tool selection and agent responses.

        Returns:
            StateGraph: The compiled LangGraph graph with the necessary nodes and edges.
        """
        graph_builder = StateGraph(State)
        graph_builder.add_node("agent", self._agent_node())
        graph_builder.add_node("select_relevant_tools", self._select_relevant_tools_node())
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            path_map=["tools", "__end__"]
        )
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("select_relevant_tools", "agent")
        graph_builder.add_edge(START, "select_relevant_tools")

        return graph_builder.compile(checkpointer=self.checkpointer)

    def _state_pruner(self, state: State) -> None:
        """
        Prunes the state by limiting the messages based on the context size and removing unused tools.

        Args:
            state (State): The current state to be pruned.
        """
        if self.disable_pruner or 'selected_tools' not in state:
            return

        used_tools = set()
        if self.context_size:
            state["messages"] = state["messages"][-self.context_size:]

        for message in state["messages"]:
            if isinstance(message, ToolMessage):
                used_tools.add(message.name)

        state["selected_tools"] = used_tools

    @staticmethod
    def context_id(thread_id: str) -> Dict[str, Dict[str, str]]:
        """
        Returns a context ID for a specific thread.

        Args:
            thread_id (str): The ID of the thread.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the thread context.
        """
        return {"configurable": {"thread_id": f"{thread_id}"}}

    @staticmethod
    def _validate_init_args(
            model: BaseChatModel,
            tools: Optional[List[Tool]],
            checkpointer: Optional[BaseCheckpointSaver],
            tool_selector: Optional[Callable[[str, int], List[Tool]]],
            top_k: int,
            context_size: Optional[int],
            disable_pruner: bool,
            prompt_template: str
    ) -> None:
        """
        Validates the initialization arguments for the AgentAmi class.

        Args:
            model (BaseChatModel): The language model to use.
            tools (Optional[List[Tool]]): A list of Tool instances.
            checkpointer (Optional[BaseCheckpointSaver]): Checkpoint saving strategy instance.
            tool_selector (Optional[Callable[[str, int], List[Tool]]]): Callable to select relevant tools.
            top_k (int): Number of top tools to consider.
            context_size (Optional[int]): Maximum context window size.
            disable_pruner (bool): Flag to disable tool pruning logic.
            prompt_template (str): Prompt template to use with the model.

        Raises:
            TypeError: If an argument is not of the expected type.
            ValueError: If an argument has an invalid value.
        """
        if not isinstance(model, BaseChatModel):
            raise TypeError("model must be an instance of BaseChatModel.")

        if tools is not None:
            if not isinstance(tools, list):
                raise TypeError("tools must be a list of Tool instances.")

        if checkpointer is not None and not isinstance(checkpointer, BaseCheckpointSaver):
            raise TypeError("checkpointer must be an instance of BaseCheckpointSaver.")

        if tool_selector is not None and not callable(tool_selector):
            raise TypeError("tool_selector must be callable if provided.")

        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be an integer greater than or equal to 1.")

        if context_size is not None:
            if not isinstance(context_size, int) or context_size <= 1:
                raise ValueError("context_size must be an integer greater than 1 if provided.")

        if not isinstance(disable_pruner, bool):
            raise TypeError("disable_pruner must be a boolean.")

        if not isinstance(prompt_template, str):
            raise TypeError("prompt_template must be a string.")
