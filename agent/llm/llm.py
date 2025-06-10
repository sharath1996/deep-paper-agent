
from abc import abstractmethod
import openai
import os
from pydantic import BaseModel
from openai import AzureOpenAI


class LLM:

    def __init__(self):
        ...
    
    @abstractmethod
    def add_system_prompt(self, param_str_systemPrompt:str):
        ...
    
    @abstractmethod
    def add_user_prompt(self, param_str_userPrompt:str):
        ...
    
    @abstractmethod
    def clear_messages(self):
        ...

    @abstractmethod
    def get_answer(self):
        ...
    
    @abstractmethod
    def get_structured_output(self, param_obj_pydanticModel: BaseModel):
        ...


class OpenAILLMInterface(LLM):

    
    def __init__(self):
    
        super().__init__()
        self.str_modelName = "gpt-4o-mini"
        self.list_messages = []
        openai.api_key = os.environ.get("OPEN_AI_API_ACCESS_KEY")
    
    def add_system_prompt(self, param_str_systemPrompt: str):
        
        self.list_messages.append({"role": "system", "content": param_str_systemPrompt})

    
    def add_user_prompt(self, param_str_userPrompt: str):
        
        self.list_messages.append({"role": "user", "content": param_str_userPrompt})

    
    def get_answer(self):
        
        local_object_response = openai.chat.completions.create(
            messages=self.list_messages,
            model=self.str_modelName,
            temperature=0.7,
            max_tokens=1000,
        )

        local_str_answer =  local_object_response.choices[0].message.content.strip()
        self.list_messages.append({"role": "assistant", "content": local_str_answer})
        return local_str_answer
    
    def get_structured_output(self, param_obj_pydanticModel:BaseModel):

        local_object_response = openai.beta.chat.completions.parse(
            messages=self.list_messages,
            model=self.str_modelName,
            temperature=0.7,
            max_tokens=1000,
            response_format=param_obj_pydanticModel
        )

        local_str_answer = local_object_response.choices[0].message.content.strip()
        self.list_messages.append({"role": "assistant", "content": local_str_answer})

        local_obj_response =  param_obj_pydanticModel.model_validate_json(local_str_answer)
        return local_obj_response

    def clear_messages(self):
        self.list_messages = []
        return True

class AzureOpenAILLMInterface(LLM):

    def __init__(self):
        super().__init__()
        
        self._obj_client = AzureOpenAI(  
		azure_endpoint=os.environ.get("AZURE_OPEN_AI_ENDPOINT"),  
		api_key=os.environ.get("AZURE_OPEN_AI_ACCESS_KEY"),  
		api_version=os.environ.get("AZURE_OPEN_AI_API_VERSION") 
		)

        self.str_modelName = "gpt-4o"
        self.list_messages = []
    
    def get_answer(self):
        
        local_object_response = self._obj_client.chat.completions.create(
            messages=self.list_messages,
            model=self.str_modelName,
            temperature=0.7,
            max_tokens=1000,
        )

        local_str_response = local_object_response.choices[0].message.content.strip()
        self.list_messages.append({"role": "assistant", "content": local_str_response})

        return local_str_response

    def get_structured_output(self, param_obj_pydanticModel:BaseModel):
        
        local_object_response = self._obj_client.beta.chat.completions.parse(
            messages=self.list_messages,
            model = self.str_modelName,
            temperature = 0.7,
            max_tokens = 1000,
            response_format=param_obj_pydanticModel
        )

        local_str_answer = local_object_response.choices[0].message.content.strip()
        self.list_messages.append({"role": "assistant", "content": local_str_answer})
        
        local_obj_response =  param_obj_pydanticModel.model_validate_json(local_str_answer)
        return local_obj_response

    def clear_messages(self):
        self.list_messages = []
        return True

    def add_system_prompt(self, param_str_systemPrompt: str):
        
        self.list_messages.append({"role": "system", "content": param_str_systemPrompt})

    def add_user_prompt(self, param_str_userPrompt: str):
        self.list_messages.append({"role": "user", "content": param_str_userPrompt})


