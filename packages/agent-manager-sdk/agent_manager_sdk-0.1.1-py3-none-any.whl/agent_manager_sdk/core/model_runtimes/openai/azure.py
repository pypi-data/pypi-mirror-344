from typing import Union

from openai import AsyncAzureOpenAI, AzureOpenAI

from ....core.model_runtimes.openai.base import OpenaiModelRuntime
from ....core.model_runtimes.openai.config import Config


class AzureModelRuntime(OpenaiModelRuntime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        api_version = kwargs.get('api_version')
        azure_endpoint = kwargs.get('azure_endpoint')
        azure_deployment = kwargs.get('azure_deployment')
        
        assert api_version is not None, 'Azure API version is required'
        assert azure_endpoint is not None, 'Azure endpoint is required'
        assert azure_deployment is not None, 'Azure deployment is required'
        
        _client = AzureOpenAI if not self.async_mode else AsyncAzureOpenAI
        
        self.client: Union[AzureOpenAI, AsyncAzureOpenAI] = _client(
            api_key=self.api_key, 
            api_version=api_version, 
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment
            )
        

class AzureUtilityMeta(type):
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

class AzureModelRuntimeSingleton(AzureModelRuntime, metaclass=AzureUtilityMeta):
    def __init__(self, async_mode=False, stream=False, **kwargs):
        super().__init__(async_mode=async_mode, stream=stream, **kwargs)