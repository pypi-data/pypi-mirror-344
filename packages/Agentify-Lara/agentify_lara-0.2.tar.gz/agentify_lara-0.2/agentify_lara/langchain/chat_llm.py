
from langchain.chat_models import *
from langchain_community.chat_models import *
from langchain_experimental.chat_models import *
from langchain_google_genai.chat_models import *

class ChatGroq:
    
    def __init__(
        self,
        api_key: str = None,
        model_name: str = "llama-3.1-8b-instant",  # corrected model name
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: int = None,
        stop: list = None,
        timeout: int = None
    ):
        from langchain_groq import ChatGroq
        import os
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Please set it or use initialize_api_key().")
        
        self.chat = ChatGroq(
            groq_api_key=api_key,
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            timeout=timeout,
            model_kwargs={'top_p': top_p}
        )
        
        self.model = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.stop = stop
        self.timeout = timeout
    
    def invoke(self, prompt: str) -> str:
        """Send a single prompt to Groq and return the model's response."""
        response = self.chat.invoke(prompt)
        return response

    def multi_invoke(self, prompts: list) -> list:
        """Send multiple prompts to Groq and return a list of responses."""
        responses = []
        for prompt in prompts:
            response = self.chat.invoke(prompt)
            responses.append(response.content)
        return responses
    def run(self,prompt:str):
        """Send a single prompt to Groq and return the model's response."""
        response = self.chat.invoke(prompt)
        return response.content

        

                


