from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)


class Evaluator:
    """
    Evaluates if the answer is likely sufficient or if we should retry with RAG.

    Returns JSON:
    {
      "needs_rag": bool,
      "feedback": "<short explanation>"
    }
    """

    SYSTEM_PROMPT = """
You are an evaluation module.

Given:
- The original USER QUERY
- The ASSISTANT ANSWER

Decide if the answer is likely:
- grounded,
- sufficiently detailed,
- and not obviously hallucinated.

If you think consulting the user's document store (RAG) would likely improve factual
accuracy or coverage, set "needs_rag": true. Otherwise, set it to false.

Return STRICT JSON:

{
  "needs_rag": true | false,
  "feedback": "<short explanation>"
}
"""

    def evaluate(self, user_query: str, answer: str) -> dict:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"USER QUERY:\n{user_query}\n\nASSISTANT ANSWER:\n{answer}",
                },
            ],
        )

        content = response.choices[0].message.content

        try:
            data = json.loads(content)
        except Exception:
            return {
                "needs_rag": False,
                "feedback": "Failed to parse evaluation; assuming no extra RAG needed.",
            }

        needs_rag = bool(data.get("needs_rag", False))
        feedback = data.get("feedback") or ""
        return {"needs_rag": needs_rag, "feedback": feedback}
