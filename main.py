from datetime import timedelta

from cachetools import cached, TTLCache
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from feedparser import parse


app = FastAPI()
templates = Jinja2Templates(directory="templates")

AWS_BLOG_CONTAINERS_URL = "https://aws.amazon.com/blogs/containers/feed/"


@cached(cache=TTLCache(maxsize=1, ttl=timedelta(minutes=5).total_seconds()))
def get_feed(url):
    feed = parse(url)
    return feed


def filter_feed(entries, filter_term: str) -> set:
    # Iterate through entries and find ones that contains the `filter_term`.
    # Return a set of unique entries.
    relevant_entries = {
        entry
        for entry in entries
        for tag in entry.tags
        if filter_term.lower() in tag.get("term", "").lower()
    }

    return relevant_entries


def get_blog_entries(filter_term: str) -> set:
    feed = get_feed(AWS_BLOG_CONTAINERS_URL)
    relevant_entries = filter_feed(feed.entries, filter_term)

    return relevant_entries


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    relevant_blog_entries = get_blog_entries(filter_term="ecs")
    return templates.TemplateResponse(
        "index.html.jinja",
        {"request": request, "blog_entries": relevant_blog_entries},
    )


@app.get("/entries", response_class=HTMLResponse)
def read_entries(request: Request, term: str = "ecs"):
    relevant_blog_entries = get_blog_entries(filter_term=term)
    return templates.TemplateResponse(
        "entries.html.jinja",
        {"request": request, "term": term, "blog_entries": relevant_blog_entries},
    )


@app.get("/json")
def read_json(term: str = "ecs"):
    relevant_blog_entries = get_blog_entries(filter_term=term)
    return {"blog_entries": relevant_blog_entries}


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")


if __name__ == "__main__":
    """
    Useful for local development. Debug with VS Code or PyCharm.
    https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger
    """
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
