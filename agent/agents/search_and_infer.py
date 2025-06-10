from textwrap import dedent
from pydantic import BaseModel, Field
from ..llm import LLMFactory
from ..tools.web_search import DuckDuckGoSearch, WebSearchResult, WebSearchInput

class SearchAndInferInput(BaseModel):
    str_task: str

class SearchAndInferOutput(BaseModel):
    str_inferredAnswer: str = Field(..., description="The inferred answer based on the search results.")
    list_webPageURLs: list[str] = Field(..., description="List of URLs from the search results that were used to infer the answer.")

class WebSearchStrings(BaseModel):
    list_searchStrings: list[str] = Field(..., description="List of search strings generated for the task.")

class SearchAndInferAgent:

    def __init__(self):
        
        self._obj_llm = LLMFactory.get_llm_interface()
        self._obj_webSearch = DuckDuckGoSearch()

    def run(self, param_obj_input:SearchAndInferInput)-> SearchAndInferOutput:
        
        """
        Executes a search and inference operation.
        
        :return: A SearchAndInferOutput object containing the inferred answer and relevant URLs.
        """
        
        local_obj_searchResults = self._search(param_obj_input)
        local_obj_inferredAnswer = self._infer(param_obj_searchInput=param_obj_input, 
                                               param_obj_searchResults=local_obj_searchResults)
        return local_obj_inferredAnswer
    
    def _search(self, param_obj_searchInput:SearchAndInferInput) -> WebSearchResult:
        
        """
        Executes a web search using the DuckDuckGo search engine.
        
        :return: A WebSearchResult object containing the search results.
        """
        local_list_webSearchResults = []
        local_obj_webSearchStrings = self._get_search_string(param_obj_searchInput)
        for local_str_searchString in local_obj_webSearchStrings.list_searchStrings:

            local_obj_webSearchInput = WebSearchInput(str_query=local_str_searchString,
                                                    str_searchEngine= "DuckDuckGo", 
                                                    max_results=5)
            local_list_webSearchResults.extend(self._obj_webSearch.search(local_obj_webSearchInput).list_webPageContent)
    
            
        return WebSearchResult(
            str_query=param_obj_searchInput.str_task,
            list_webPageContent=local_list_webSearchResults,
            int_totalResults=len(local_list_webSearchResults)
        )
        


        
        
    def _get_search_string(self, param_obj_searchInput: SearchAndInferInput) -> WebSearchStrings:
        """
        Constructs a search string based on the input query.
        
        :param param_obj_searchInput: The input parameters for the search.
        :return: A formatted search string.
        """
        self._obj_llm.clear_messages()
        local_str_sytemPrompt = dedent("""
            You are a helpful assistant that enables the user to search the web with right keywords and search terms.
            You will be given a task string, you need to return the appropriate search strings that can be used to search in the web. 
            You should always try to include the keywords that help us in finding the official documentation or relevant information sources.
            The browser we are using is DuckDuckGo, so plan your search strings accordingly""")
        
        self._obj_llm.add_system_prompt(local_str_sytemPrompt)
        local_str_userPrompt = dedent(f"""
            Here is the task: {param_obj_searchInput.str_task}
            Please return a search string that can be used to search the web.
            The search string should be concise and relevant to the query.
            You should only return the search string, nothing else.""")
        self._obj_llm.add_user_prompt(local_str_userPrompt)
        local_obj_webSearchString = self._obj_llm.get_structured_output(WebSearchStrings)
        return local_obj_webSearchString
    

    def _infer(self, param_obj_searchInput:SearchAndInferInput, param_obj_searchResults: WebSearchResult) -> SearchAndInferOutput:

        """
        """
        self._obj_llm.clear_messages()
        local_str_sytemPrompt = dedent("""
            You are a helpful assistant that can perform the task given to you from web search results.
            You will be given a task and the search results, you need to return the completed task.
            The response should be concise and relevant to the query.
            You should only use the information from the search results to infer the answer and not any internal knowledge that you may have.
            You should only return the answer, nothing else.""")
        self._obj_llm.add_system_prompt(local_str_sytemPrompt)
        self._obj_llm.add_user_prompt(f"The task is: {param_obj_searchInput.str_task}")

        local_str_searchResults = ""

        for local_obj_webPageContent in param_obj_searchResults.list_webPageContent:
            local_str_searchResults += f"Title: {local_obj_webPageContent.str_webPageTitle}\n"
            local_str_searchResults += f"Content: {local_obj_webPageContent.str_webPageContent}\n"
            local_str_searchResults += f"URL: {local_obj_webPageContent.str_webPageUrl}\n\n"
        
        self._obj_llm.add_user_prompt(f"The search results are:\n{local_str_searchResults}")
        local_obj_inferredAnswer = self._obj_llm.get_structured_output(SearchAndInferOutput)
        return local_obj_inferredAnswer