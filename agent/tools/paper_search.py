import arxiv
from pydantic import BaseModel, Field



class PaperSearchInput(BaseModel):
    """
    Represents the input for a paper search.
    """
    str_query: str = Field(..., description="The search query to be executed")
    int_numberOfResults: int = Field(10, description="Number of results to return from the search")
    str_paperSource: str = Field(..., description="The source of the papers to be searched (e.g., IEEE, Arxiv)")


class PaperResult(BaseModel):
    """
    Represents the result of a paper search.
    """
    str_title: str = Field(..., description="Title of the paper")
    str_url: str = Field(..., description="URL of the paper")
    str_abstract: str = Field(..., description="Abstract of the paper")
    str_fullText:str = Field(..., description="Full text of the paper")
    list_authors: list[str] = Field(..., description="List of authors of the paper")
    str_publishedDate: str = Field(..., description="Publication date of the paper")


class PaperSearchResult(BaseModel):
    """
    Represents the result of a paper search.
    """
    str_query: str = Field(..., description="The search query used for the paper search")
    list_paperResults: list[PaperResult] = Field(..., description="List of paper results found in the search")
    int_totalResults: int = Field(..., description="Total number of results found for the search query")

class PaperSearch:

    def __init__(self):
        ...
    
    def search(self):
        ...

class IEEEPaperSearch(PaperSearch):
    """
    A class that implements paper search functionality for IEEE papers.
    """

    def __init__(self):
        super().__init__()

    def search(self, query: str, num_results: int = 10) -> list:
        """
        Executes a paper search on IEEE Xplore based on the provided query.

        :param query: The search query to be executed.
        :param num_results: The number of results to return from the search.
        :return: A list of dictionaries containing the search results.
        """
        # Placeholder for actual implementation
        return [{"title": "Sample Paper", "url": "https://ieeexplore.ieee.org/document/1234567"}] * num_results


class ArxivPaperSearch(PaperSearch):
    """
    A class that implements paper search functionality for Arxiv papers.
    """

    def __init__(self):
        
        super().__init__()
        
        self.obj_client = arxiv.Client()

    def search(self, param_obj_searchInput:PaperSearchInput) -> PaperSearchResult:
        """
        Executes a paper search on Arxiv based on the provided query.

        :param query: The search query to be executed.
        :param num_results: The number of results to return from the search.
        :return: A list of dictionaries containing the search results.
        """
        local_obj_search = arxiv.Search(
            query=f"abs:{param_obj_searchInput.str_query}",
            max_results=param_obj_searchInput.int_numberOfResults,
            sort_by=arxiv.SortCriterion.Relevance
        )

        local_obj_results = self.obj_client.results(local_obj_search)

        list_paper_results = []
        for result in local_obj_results:
            list_paper_results.append(
                PaperResult(
                    str_title=result.title,
                    str_url=result.entry_id,
                    str_abstract=result.summary,
                    str_fullText=result.summary,  # Placeholder for full text
                    list_authors=[author.name for author in result.authors],
                    str_publishedDate=result.published.date().isoformat()
                )
            )
        
        return PaperSearchResult(
            str_query=param_obj_searchInput.str_query,
            list_paperResults=list_paper_results,
            int_totalResults=len(list_paper_results)
        )