from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    results = []
    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            title = item.get("title", "No title")
            body = item.get("body", "")
            href = item.get("href", "")
            results.append(f"Title: {title}\nSnippet: {body}\nURL: {href}")
    return "\n\n".join(results) if results else "No web results found."
