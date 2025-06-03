# Search for contents in confluences
from pydantic import BaseModel, Field, SerializeAsAny

class ConfluencePageResult(BaseModel):
    """
    Represents a single page result from a Confluence search.
    """
    str_pageTitle: str = Field(..., description="Title of the Confluence page")
    str_pageUrl: str = Field(..., description="URL of the Confluence page")
    str_pageContent: str = Field(..., description="Excerpt or summary of the Confluence page content")

class ConfluenceSearchResult(BaseModel):
    """
    Represents the result of a Confluence search.
    """
    str_query: str = Field(..., description="The search query used for the Confluence search")
    list_pageTitles: SerializeAsAny[list[ConfluencePageResult]] = Field(..., description="List of page titles found in the search")
    int_totalResults: int = Field(..., description="Total number of results found for the search query")

class ConfluenceSearchInput(BaseModel):
    """
    Represents the input for a Confluence search.
    """
    str_query: str = Field(..., description="The search query to be executed in Confluence")
    str_spaceKey: str = Field(..., description="The key of the Confluence space to search in")
    str_token: str = Field(..., description="Authentication token for Confluence API")