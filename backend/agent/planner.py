from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)


class Planner:
    """
    LLM-based planner that decides:
      - Should we answer directly?
      - Should we call the RAG pipeline?
      - (Optionally) Should we call a registered tool?

    It MUST return a JSON object like:

    {
      "action": "answer_direct" | "rag_query" | "use_tool",
      "tool_name": "<optional tool name or null>",
      "query": "<query to use for the chosen path>",
      "reason": "<short explanation>"
    }
    """

    SYSTEM_PROMPT = """
You are a planning module for an AI assistant th
Uses an LLM-based planner to decide:

"direct" → just answer from the model

"rag" → use RAG with your vectorat has:
- A RAG pipeline over user documents.
- Optional tools for working with code (repo_read_file, repo_run_tests, repo_apply_patch).
- A normal LLM that can answer general questions.

Decide the best action for each user query.

Rules:

1. Use "rag_query" when:
   - The user asks about documents, PDFs, notes, research, policies, specs, APIs, codebases
     or anything likely stored in their knowledge base.
   - The answer depends on factual or detailed information that *might* be in those docs.

2. Use "answer_direct" when:
   - The question is generic, conversational, or conceptual (e.g., "What is a vector DB?",
     "Explain RAG", "What is ACID?").
   - You can answer confidently from general knowledge and it is not about *their* specific data.

3. Use "use_tool" ONLY when:
   - The user clearly asks you to operate on code or a repo, such as:
       - "Open file X and explain it."
       - "Run the tests."
       - "Apply a patch to this file."
   - And you pick a tool_name from this allowed set:
       - "repo_read_file"
       - "repo_list_files"
       - "repo_search_code"
       - "repo_apply_patch"
       - "repo_run_tests"

4. Never invent new tool names. If no suitable tool exists, prefer "rag_query" or "answer_direct".

Return STRICTLY valid JSON in this format (no comments, no extra keys):

{
  "action": "answer_direct" | "rag_query" | "use_tool",
  "tool_name": "repo_read_file" | "repo_list_files" | "repo_search_code" | "repo_run_tests" | "repo_apply_patch" | null,
  "query": "<possibly rewritten query>",
  "reason": "<short reason>"
}
"""

    def plan(self, user_query: str) -> dict:
        """Call the LLM planner and return a sanitized plan dict."""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
            ],
        )

        content = response.choices[0].message.content

        # Robust JSON parsing + fallback
        try:
            plan = json.loads(content)
        except Exception:
            # Fallback: default to RAG
            return {
                "action": "rag_query",
                "tool_name": None,
                "query": user_query,
                "reason": "Failed to parse planner output, defaulting to RAG.",
            }

        # --- Sanitization ---
        action = plan.get("action", "rag_query")
        if action not in ("answer_direct", "rag_query", "use_tool"):
            action = "rag_query"

        tool_name = plan.get("tool_name")
        allowed_tools = {"repo_read_file", "repo_run_tests", "repo_apply_patch"}

        if action == "use_tool":
            if tool_name not in allowed_tools:
                # Invalid tool -> fall back to RAG instead of crashing
                action = "rag_query"
                tool_name = None
        else:
            tool_name = None

        query = plan.get("query") or user_query
        reason = plan.get("reason") or "No reason provided."

        return {
            "action": action,
            "tool_name": tool_name,
            "query": query,
            "reason": reason,
        }
