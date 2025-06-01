from agent.tools.web_search import LangSearch, WebSearchInput, TavilySearch
import json

def test_lang_search():
    # Create an instance of the GoogleWebSearch class
    local_obj_searchEngine = LangSearch()

    # Define the search input parameters
    local_obj_input = WebSearchInput(
        str_query="Latest trends in edge computing for AI",
        str_searchEngine="Langsearch",
        int_numberOfResults=10
    )

    # Perform the search
    local_obj_searchResult = local_obj_searchEngine.search(local_obj_input)

    with open(".results/test_search_results.json", "w") as f:
        json.dump(local_obj_searchResult.model_dump(), f, indent=4)

def test_tavily_search():
    # Create an instance of the TavilyClient class
    local_obj_searchEngine = TavilySearch()

    # Define the search input parameters
    local_obj_input = WebSearchInput(
        str_query="Latest trends in edge computing for AI",
        str_searchEngine="Tavily",
        int_numberOfResults=10
    )

    # Perform the search
    local_obj_searchResult = local_obj_searchEngine.search(local_obj_input)

    with open(".results/test_tavily_search_results.json", "w") as f:
        json.dump(local_obj_searchResult.model_dump(), f, indent=4)