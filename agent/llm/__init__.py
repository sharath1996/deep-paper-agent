from .llm import LLM, AzureOpenAILLMInterface, OpenAILLMInterface
import os

class LLMFactory:

    @staticmethod
    def get_llm_interface() -> LLM:
        local_str_modelProvider = os.environ.get("MODEL_PROVIDER", "openai")
        if local_str_modelProvider == "openai":
            return OpenAILLMInterface()
        elif local_str_modelProvider == "azure_openai":
            return AzureOpenAILLMInterface()
        else:
            raise ValueError(f"Unsupported LLM type: {local_str_modelProvider}")

