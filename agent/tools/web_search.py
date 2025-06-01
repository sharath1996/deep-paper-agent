from abc import abstractmethod
import json
from pydantic import BaseModel, Field
import os
import requests
from tavily import TavilyClient

class WebPageContent(BaseModel):
    """
    Represents the results of a web search.

    """
    str_webPageTitle: str = Field(..., description="Title of the web page")
    str_webPageContent: str = Field(..., description="Content of the web page")
    str_webPageUrl: str = Field(..., description="URL of the web page")

class WebSearchResult(BaseModel):
    """
    Represents the result of a web search.

    """
    str_query: str = Field(..., description="The search query")
    list_webPageContent: list[WebPageContent] = Field(..., description="List of web page contents found in the search")
    int_totalResults: int = Field(..., description="Total number of results found for the search query")

class WebSearchInput(BaseModel):
    """
    Represents the input for a web search.

    """
    str_query: str = Field(..., description="The search query to be executed")
    str_searchEngine: str = Field(..., description="The search engine to be used for the search")
    int_numberOfResults: int = Field(10, description="Number of results to return from the search")


class WebSearch():

    def __init__(self):
        ...
    
    @abstractmethod
    def search(self, param_obj_webSearchInput:WebSearchInput)->WebSearchResult:
        """
        Executes a web search based on the provided input.

        :param param_obj_webSearchInput: The input parameters for the web search.
        :return: A WebSearchResult object containing the search results.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class LangSearch(WebSearch):
    """
    A class that implements web search functionality using the LangChain framework.
    """

    def __init__(self):
        super().__init__()

    def search(self, param_obj_webSearchInput: WebSearchInput) -> WebSearchResult:
        """
        Executes a web search using the LangChain framework.

        :param param_obj_webSearchInput: The input parameters for the web search.
        :return: A WebSearchResult object containing the search results.
        """
        # Placeholder for actual implementation
        return self._get_search_results(
            param_str_query=param_obj_webSearchInput.str_query,
            param_int_numberOfResults=param_obj_webSearchInput.int_numberOfResults
        )
    
    def _get_search_results(self, param_str_query:str, param_int_numberOfResults:int) -> WebSearchResult:
        """
        Placeholder for a method that would interact with a search engine API to get results.

        :param param_str_query: The search query.
        :param param_int_numberOfResults: The number of results to return.
        :return: A list of WebPageContent objects.
        """
        # This is a placeholder implementation
        local_str_endPointUrl = "https://api.langsearch.com/v1/web-search"
        local_dict_payLoad = {
            "query": param_str_query,
            "freshness" : "oneMonth",
            "summary" : True,
            "count" : param_int_numberOfResults
        }

        local_dict_headers = {
            "Authorization": f"Bearer {os.getenv('LANGSEARCH_API_KEY')}",
            "Content-Type": "application/json"
        }

        local_obj_response = requests.post(local_str_endPointUrl, json=local_dict_payLoad, headers=local_dict_headers)

        if local_obj_response.status_code == 200:
            local_dict_response = local_obj_response.json()
            
            local_list_webPages = local_dict_response['data']['webPages']['value']
            local_list_webPagesObjects = []
            for local_dict_webPage in local_list_webPages:
                local_obj_webPageContent = WebPageContent(
                    str_webPageTitle=local_dict_webPage['name'],
                    str_webPageContent=local_dict_webPage['summary'],
                    str_webPageUrl=local_dict_webPage['displayUrl']
                )
                local_list_webPagesObjects.append(local_obj_webPageContent)
            
            return WebSearchResult(
                str_query=local_dict_response['data']['queryContext']['originalQuery'],
                list_webPageContent=local_list_webPagesObjects,
                int_totalResults=len(local_list_webPagesObjects)
            )



                

class TavilySearch(WebSearch):
    """
    A class that implements web search functionality using the Tavily framework.
    """

    def __init__(self):
        super().__init__()

    def search(self, param_obj_webSearchInput: WebSearchInput) -> WebSearchResult:
        """
        Executes a web search using the Tavily framework.

        :param param_obj_webSearchInput: The input parameters for the web search.
        :return: A WebSearchResult object containing the search results.
        """
        # Placeholder for actual implementation
        local_obj_tavilyClient = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
        local_dict_response = local_obj_tavilyClient.search(
            search_depth="advanced",
            query=param_obj_webSearchInput.str_query,
            count=param_obj_webSearchInput.int_numberOfResults,
            time_range="week",
            include_raw_content=True)

        with open('tavily_response.json', 'w') as local_file:
            json.dump(local_dict_response, local_file, indent=4)
        # return an empty result for now
        local_list_webPagesObjects = []
        
        for local_dict_result in local_dict_response['results']:
            local_obj_webPageContent = WebPageContent(
                str_webPageTitle=local_dict_result["title"],
                str_webPageContent=local_dict_result["raw_content"],
                str_webPageUrl=local_dict_result["url"]
            )
            local_list_webPagesObjects.append(local_obj_webPageContent)

        return WebSearchResult(
            str_query=param_obj_webSearchInput.str_query,
            list_webPageContent=local_list_webPagesObjects,
            int_totalResults=len(local_list_webPagesObjects)
        )