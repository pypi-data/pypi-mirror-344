from typing import Any

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from saptiva_agents import DEFAULT_LANG, CONTENT_CHARS_MAX


async def get_weather(city: str) -> str: # Async tool is possible too.
    """
    Get weather from a city.
    :param city: City name
    :return: Weather information
    """
    return f"The weather in {city} is 72 degree and sunny."


async def wikipedia_search(query: str) -> Any:
    """
    Function for searching information on Wikipedia without using `BaseTool`.

    Make sure to install Wikipedia:
        pip install wikipedia
    """
    try:
        api_wrapper = WikipediaAPIWrapper(doc_content_chars_max=CONTENT_CHARS_MAX, lang=DEFAULT_LANG, wiki_client="wikipedia")
        tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        result = tool.invoke({"query": query})

        return result

    except Exception as e:
        raise e
