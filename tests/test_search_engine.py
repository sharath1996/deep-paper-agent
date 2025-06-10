from agent.tools.web_search import LangSearch, WebSearchInput, TavilySearch, DuckDuckGoSearch
from agent.tools.paper_search import ArxivPaperSearch,CrossRefPaperSearch, PaperSearchInput
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


def test_arxiv_search():

    # Create an instance of the ArxivPaperSearch class
    local_obj_searchEngine = ArxivPaperSearch()

    # Define the search input parameters
    local_obj_input = PaperSearchInput(
        str_query="edge computing optimizations for edgeAI",
        str_searchEngine="Arxiv",
        int_numberOfResults=10,
        str_paperSource="Arxiv"
    )
    # Perform the search
    local_obj_searchResult = local_obj_searchEngine.search(local_obj_input)

    with open(".results/test_arxiv_search_results.json", "w") as f:
        json.dump(local_obj_searchResult.model_dump(), f, indent=4)

def test_duckduckgo_search():
    # Create an instance of the DuckDuckGoSearch class
    local_obj_searchEngine = DuckDuckGoSearch()

    # Define the search input parameters
    local_obj_input = WebSearchInput(
        str_query="Latest trends in edge computing for AI",
        str_searchEngine="DuckDuckGo",
        int_numberOfResults=10
    )

    # Perform the search
    local_obj_searchResult = local_obj_searchEngine.search(local_obj_input)

    with open(".results/test_duckduckgo_search_results.json", "w") as f:
        json.dump(local_obj_searchResult.model_dump(), f, indent=4)

def test_crossref_search():
    # Create an instance of the CrossRefPaperSearch class
    local_obj_searchEngine = CrossRefPaperSearch()

    # Define the search input parameters
    local_obj_input = PaperSearchInput(
        str_query="edge computing optimizations for edgeAI",
        str_searchEngine="CrossRef",
        int_numberOfResults=10,
        str_paperSource="CrossRef"
    )
    
    # Perform the search
    local_obj_searchResult = local_obj_searchEngine.search(local_obj_input)

    with open(".results/test_crossref_search_results.json", "w") as f:
        json.dump(local_obj_searchResult.model_dump(), f, indent=4)