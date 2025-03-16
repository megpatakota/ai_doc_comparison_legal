from openai import OpenAI


def embed(text: str, model: str = "text-embedding-3-large") -> list[float]:
    """Embed text using the OpenAI API."""
    response = OpenAI().embeddings.create(input=text, model=model)
    return response.data[0].embedding


def embed_batch(
    texts: list[str], model: str = "text-embedding-3-large"
) -> list[list[float]]:
    """Embed a batch of texts using the OpenAI API."""
    response = OpenAI().embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]
