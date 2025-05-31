from agent.tools.web_search import LangSearch, WebSearchInput
import json

def test_lang_search():
    # Create an instance of the GoogleWebSearch class
    search_engine = LangSearch()

    # Define the search input parameters
    search_input = WebSearchInput(
        str_query="Latest trends in edge computing for AI",
        str_searchEngine="Langsearch",
        int_numberOfResults=10
    )

    # Perform the search
    search_result = search_engine.search(search_input)

    with open(".results/test_search_results.json", "w") as f:
        json.dump(search_result.model_dump(), f, indent=4)