

from textwrap import dedent
from pydantic import BaseModel, Field
from trafilatura import fetch_url, extract
import logging
from playwright.sync_api import sync_playwright
from ..llm import LLMFactory

class WebPageSummarizerInput(BaseModel):
    """
    Represents the input for summarizing a web page.
    
    Attributes:
        str_url (str): The URL of the web page to summarize.
    """
    str_url: str = Field(..., description="The URL of the web page to summarize")
    str_webSearchQuery: str = Field(..., description="The query that you want to search for in the web page content")

class WebPageSummarizerOutput(BaseModel):
    """
    Represents the output of a web page summarization.
    
    Attributes:
        str_summary (str): The summary of the web page content.
    """
    str_summary: str | None = Field(..., description="The summary of the web page content")


class WebPageSummarizer:
    """
    A class to summarize web pages.
    """

    def __init__(self, url: str):
        self.url = url

    def summarize(self, param_obj_input:WebPageSummarizerInput) -> WebPageSummarizerOutput:
        """
        Summarizes the web page at the given URL.
        """
        if not param_obj_input.str_url:
            raise ValueError("The URL cannot be empty.")
        
        # Fetch the full page content as markdown
        local_str_fullText = self._get_full_page_as_markdown(param_obj_input.str_url)
        
        if local_str_fullText is None:
            return WebPageSummarizerOutput(str_summary=None)
        # Extract and summarize the content
        local_obj_output = self._extract_and_summarize(local_str_fullText, param_obj_input.str_webSearchQuery)
        logging.info(f"Extracted content for URL {param_obj_input.str_url} with query {param_obj_input.str_webSearchQuery}")
        return local_obj_output
    
    def _get_full_page_as_markdown(self, param_str_url:str) -> str:
        """
        Retrieves the full content of the web page as markdown.
        
        Args:
            param_str_url (str): The URL of the web page to retrieve.
        
        Returns:
            str: The content of the web page in markdown format.
        """
        # use playwright to fetch and extract the content only if it is html page and not any pdf or any other format that trafilatura can not
        
        local_obj_page = None
        with sync_playwright() as playwright:
            local_obj_browser = playwright.chromium.launch(headless=True)
            local_obj_context = local_obj_browser.new_context()
            local_obj_page = local_obj_context.new_page()
            try:
                local_obj_page.goto(param_str_url, wait_until='networkidle')
                local_obj_contents = local_obj_page.content()
            except Exception as e:
                logging.error(f"Failed to fetch the URL {param_str_url}: {e}")
                return None
            
            # close the browser context and browser
            



        if local_obj_contents is None:
            raise ValueError(f"Failed to fetch the URL: {param_str_url}")
        
        local_str_content = extract(local_obj_contents, include_comments=False, include_tables=True, include_formatting=True, output_format='markdown')
        if local_str_content is None:
            raise ValueError(f"Failed to extract content from the URL: {param_str_url}")
    
        return local_str_content.strip()
        
    def _extract_and_summarize(self, param_str_fullText:str, param_str_webSearchQuery:str) -> WebPageSummarizerOutput:
        """
        Extracts and summarizes the content of the web page.
        
        Args:
            param_str_url (str): The URL of the web page to summarize.
            param_str_webSearchQuery (str): The query to search for in the web page content.
        
        Returns:
            str: The summary of the web page content.
        """
        
        local_obj_llm = LLMFactory.get_llm_interface()

        local_str_systemPrompt = dedent("""
        You are a content extraction expert, who can extract the content of a web page related to a specific query.
        You will be given the full text of a source and a query.
        You need to return the content of the source that is relevant to the qeury in the markdown format.
        Your responses will be in the json format
        """)

        local_str_userPrompt = f"Full text : {param_str_fullText}\n\nQuery: {param_str_webSearchQuery}\n\nPlease extract the relevant content in markdown format."
        local_str_response = local_obj_llm.clear_messages()
        local_obj_llm.add_system_prompt(local_str_systemPrompt)
        local_obj_llm.add_user_prompt(local_str_userPrompt)
        local_str_response = local_obj_llm.get_structured_output(WebPageSummarizerOutput)

        return local_str_response