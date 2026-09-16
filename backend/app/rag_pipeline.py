from app.vector_store import load_vector_store
from app.llm import BedrockLLM

def get_answer(query):
    db = load_vector_store()
    docs = db.similarity_search(query, k=5)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a medical AI assistant.

RULES:
- Answer ONLY from the provided context
- If answer is not in context, say "I don't know"
- Do NOT hallucinate
- Keep answer clear and short

Context:
{context}

Question:
{query}

Answer:
"""

    llm = BedrockLLM()
    answer = llm.generate(prompt)

    return answer, docs
