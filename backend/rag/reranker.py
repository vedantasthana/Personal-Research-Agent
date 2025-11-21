from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class Reranker:
    def rerank(self, query: str, passages: list[str]):
        if not passages:
            return []

        # Format passages for LLM
        numbered = "\n\n".join(
            [f"Passage {i+1}:\n{p}" for i, p in enumerate(passages)]
        )

        prompt = f"""
You are a ranking model. Rank the following passages by relevance to the query.

Query:
{query}

Passages:
{numbered}

Return ONLY a list of passage numbers in descending order of relevance.
Example: [3,1,2]
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content
        numbers = eval(text)  # passages returned as [2,1,3]

        # Convert numbers into actual passages
        return [passages[i-1] for i in numbers]
