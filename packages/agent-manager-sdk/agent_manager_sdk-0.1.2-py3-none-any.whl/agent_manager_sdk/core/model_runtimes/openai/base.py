from typing import Dict, List, Union

from openai import AsyncOpenAI, OpenAI

from ....core.model_runtimes.base import ModelRuntime
from ....core.model_runtimes.openai.config import Config


class OpenaiModelRuntime(ModelRuntime):
    
    def __init__(self,
                 model,
                 api_key: str,
                 async_mode: bool = False,
                 *args,
                 **kwargs       
                 ):
        self.async_mode = async_mode
        self.api_key = api_key
        self.model = model
        
        _client = OpenAI if not async_mode else AsyncOpenAI
        
        self.client: Union[OpenAI, AsyncOpenAI] = _client(api_key=api_key)
        
        
    def run(self, 
            messages: List[Dict],
            temperature: float = 0.5,
            max_tokens: int = 4096,
            top_p: float = 1.0,
            return_complete=False
            ) -> str:
        
        result = self.client.chat.completions.create(model=self.model,
                                                messages=messages,
                                                temperature=temperature,
                                                max_tokens=max_tokens,
                                                top_p=top_p)
        
        return result.choices[0].message.content if not return_complete else result
    
    def sync_stream(self,
                    messages: List[Dict],
                    temperature: float = 0.5,
                    max_tokens: int = 4096,
                    top_p: float = 1.0,
                    return_complete=False
                    ):
        
        result = self.client.chat.completions.create(model=self.model,
                                                messages=messages,
                                                temperature=temperature,
                                                max_tokens=max_tokens,
                                                top_p=top_p,
                                                stream=True)
        full_value = ''
        for response in result:
            try:
                value = response.choices[0].delta.content
                if value:
                    full_value += value
                    yield full_value if not return_complete else response
            except IndexError:
                continue
    
    async def arun(self, 
            messages: List[Dict],
            temperature: float = 0.5,
            max_tokens: int = 4096,
            top_p: float = 1.0,
            return_complete=False
            ) -> str:
        
        result = await self.client.chat.completions.create(model=self.model,
                                            messages=messages,
                                            temperature=temperature,
                                            max_tokens=max_tokens,
                                            top_p=top_p)
        
        return result.choices[0].message.content if not return_complete else result
    
    async def async_stream(self,
                    messages: List[Dict],
                    temperature: float = 0.5,
                    max_tokens: int = 4096,
                    top_p: float = 1.0,
                    return_complete=False
                    ):
        
        result = await self.client.chat.completions.create(model=self.model,
                                                messages=messages,
                                                temperature=temperature,
                                                max_tokens=max_tokens,
                                                top_p=top_p,
                                                stream=True)
        
        full_value = ''
        async for response in result:
            try:
                value = response.choices[0].delta.content
                if value:
                    full_value += value
                    yield full_value if not return_complete else response
            except IndexError:
                continue

class OpenAIUtilityMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        settings = ''
        stream = f'stream_{kwargs.get("stream", False)}'
        async_mode = f'async_{kwargs.get("async_mode", False)}'
        settings = f'{stream}_{async_mode}'
        
        if settings not in cls._instances:
            
            instance = super().__call__(*args,
                                        model=Config.OPENAI_MODEL,
                                        api_key=Config.OPENAI_API_KEY,
                                        azure_endpoint=Config.OPENAI_API_BASE,
                                        api_version=Config.OPENAI_API_VERSION,
                                        azure_deployment=Config.OPENAI_DEPLOYMENT_ID,
                                        **kwargs)
            cls._instances[settings] = instance
        return cls._instances[settings]
            
class OpenAIModelRuntimeSingleton(OpenaiModelRuntime, metaclass=OpenAIUtilityMeta):
    def __init__(self, async_mode=False, stream=False, **kwargs):
        super().__init__(async_mode=async_mode, stream=stream, **kwargs)