from dotenv import load_dotenv
import os

load_dotenv('secret.env')

class Config:
    # Add your configuration variables here if needed
    
    WORKFLOW_ENDPOINT = os.getenv('WORKFLOW_ENDPOINT')