from core.model_runtimes.openai.azure import AzureModelRuntime
from core.model_runtimes.openai.config import Config


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