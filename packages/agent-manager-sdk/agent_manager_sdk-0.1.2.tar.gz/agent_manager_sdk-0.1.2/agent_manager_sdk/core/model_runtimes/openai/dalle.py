import json
from typing import Dict, List, Union

from openai import AsyncOpenAI, OpenAI

from ....core.model_runtimes.base import ModelRuntime
from ....core.model_runtimes.openai.config import Config


class DalleOpenaiModelRuntime(ModelRuntime):
    
    def __init__(self,
                 model,
                 api_key: str,
                 *args,
                 **kwargs       
                 ):
        self.api_key = api_key
        self.model = model
        
        _client = OpenAI
        self.client: OpenAI = _client(api_key=api_key)

        
    def run(self, 
            prompt: str
            ) -> str:
        
        result = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            n=1
        )

        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        
        return image_url

class DalleUtilityMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        settings = ''
        stream = f'stream_{kwargs.get("stream", False)}'
        async_mode = f'async_{kwargs.get("async_mode", False)}'
        settings = f'{stream}_{async_mode}'
        
        if settings not in cls._instances:
            instance = super().__call__(*args,
                                        model=Config.DALLE_MODEL,
                                        api_key=Config.DALLE_API_KEY,
                                        azure_endpoint=Config.DALLE_API_BASE,
                                        api_version=Config.DALLE_API_VERSION,
                                        azure_deployment=Config.DALLE_DEPLOYMENT_ID,
                                        **kwargs)
            cls._instances[settings] = instance
        return cls._instances[settings]

class DalleModelRuntimeSingleton(DalleOpenaiModelRuntime, metaclass=DalleUtilityMeta):
    def __init__(self, async_mode=False, stream=False, **kwargs):
        super().__init__(async_mode=async_mode, stream=stream, **kwargs)