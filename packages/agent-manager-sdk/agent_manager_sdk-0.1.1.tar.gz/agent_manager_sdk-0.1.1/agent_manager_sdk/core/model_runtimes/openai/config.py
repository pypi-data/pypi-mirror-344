import os

# Create a config class from above information, use os.getenv to get the openai key, model, api type, api base, api version, deployment id

class Config:
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
    OPENAI_DEPLOYMENT_ID = os.getenv("OPENAI_DEPLOYMENT_ID")
    
    DALLE_MODEL = os.getenv("DALLE_MODEL")
    DALLE_API_KEY = os.getenv("DALLE_API_KEY")
    DALLE_API_BASE = os.getenv("DALLE_API_BASE")
    DALLE_API_VERSION = os.getenv("DALLE_API_VERSION")
    DALLE_DEPLOYMENT_ID = os.getenv("DALLE_DEPLOYMENT_ID")
    
    