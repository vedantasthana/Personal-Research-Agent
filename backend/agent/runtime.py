from agent.planner import Planner
from agent.evaluator import Evaluator
from rag.retriever import Retriever
from rag.context_builder import build_context
from agent.tools import registry
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


class AgentRuntime:
    def __init__(self) -> None:
        self.planner = Planner()
        self.evaluator = Evaluator()
        self.retriever = Retriever()

    # ------------------------
    # Answer strategies
    # ------------------------
    def answer_direct(self, query: str) -> str:
        """LLM-only answering (no RAG, no tools)."""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer using your own knowledge.",
                },
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content

    def answer_with_rag(self, query: str) -> str:
        """Use retriever + context builder + LLM for grounded answer."""
        # Prefer hybrid if implemented; fall back to vector search otherwise
        if hasattr(self.retriever, "hybrid_search"):
            chunks = self.retriever.hybrid_search(query, k=5)
        else:
            # Simple vector-only
            chunks = self.retriever.retrieve(query, k=5)

        context = build_context(chunks)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content

    def use_tool(self, tool_name: str, tool_input: str) -> str:
        """Dispatch to a registered tool."""
        # If somehow tool_name is None or invalid, gracefully fall back
        if not tool_name:
            return self.answer_direct(
                f"Tool name was missing, falling back to direct answer. Original input: {tool_input}"
            )

        try:
            return registry.call(tool_name, tool_input)
        except KeyError:
            # Safety: don't crash if planner suggested something wrong
            return self.answer_with_rag(
                f"Tool '{tool_name}' was not found. Please answer using RAG. Original input: {tool_input}"
            )

    # ------------------------
    # Main entrypoint
    # ------------------------
    def run(self, user_query: str) -> str:
        """
        Full agent loop:
        1. Planner: decide action + (optional) tool.
        2. Execute: direct / RAG / tool.
        3. Evaluator: decide if we need a RAG retry.
        """

        # 1. Plan
        plan = self.planner.plan(user_query)
        action = plan["action"]
        tool_name = plan.get("tool_name")
        query = plan["query"]

        # 2. Execute according to plan
        if action == "rag_query":
            answer = self.answer_with_rag(query)
        elif action == "use_tool":
            answer = self.use_tool(tool_name, query)
        else:  # "answer_direct"
            answer = self.answer_direct(query)

        # 3. Evaluate answer quality / groundedness
        evaluation = self.evaluator.evaluate(user_query, answer)

        if evaluation["needs_rag"] and action != "rag_query":
            # Retry using RAG if evaluator thinks we need it
            return self.answer_with_rag(user_query)

        return answer
