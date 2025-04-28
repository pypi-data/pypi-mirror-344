import json
import os
import threading

import requests
from dotenv import load_dotenv
from flask import Response, stream_with_context
from flask_restful import Resource, marshal_with, reqparse
from pinecone import Pinecone

from ....app_extensions.db_ext import db
from ....controllers.console import api
from ....core.model_runtimes.openai.azure import AzureModelRuntimeSingleton
from ....core.retrieval_agent.prompts import (
    FINAL_OUTPUT_SYSTEM,
    FINAL_OUTPUT_USER,
    PLANNING_SYSTEM,
    PLANNING_USER,
)

load_dotenv('secret.env')

jina_api_key = os.getenv('JINA_API_KEY')
hugging_face_api_key = os.getenv('HUGGINGFACE_API_KEY')
print(jina_api_key)
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


def encode_queries(terms):
    vectors = []
    for term in terms:
        payload = {"inputs": [term],
                # "model": "jina-clip-v1",
                #     "embedding_type": "float",
                "options":{"wait_for_model":True}
    }
        headers = {"Authorization": f"Bearer {hugging_face_api_key}",
                "Content-Type": "application/json",}
        
        response = requests.post(API_URL, headers=headers, json=payload)
        response = response.json()[0]
        vectors.append(response)
    return vectors

api_key = os.getenv('PINECONE_API_KEY')

def search_relevant_terms(terms):
    
    # for term in terms:
    #     dotagent_file = search_relevant_terms(term)
    
    all_data = []
    
    workflows = ['content_generator', 'image_generator', 'website_generator']
    for workflow in workflows:
        with open(f'agents/{workflow}.json') as f:
            data = json.load(f)
            all_data.append(data)
    
    pinecone = Pinecone(api_key=api_key)

    pinecone_index = pinecone.Index("agentpackagesearch4")
    vectors = encode_queries(['Cats', 'Dogs', 'Python', 'Jack'])
    vectors = [{ 'id':str(idx), 'values':value } for idx, value in enumerate(vectors)]
    print(vectors)
    pinecone_index.upsert(vectors=vectors, namespace='agentpackagesearch2')
    results = []
    query_vector = encode_queries(terms)
    print(len(query_vector))
    print(len(query_vector[0]))
    try:
        query_results = pinecone_index.query(vector=query_vector, top_k=5, namespace="agentpackagesearch2")
    except:
        return {}
    for match in query_results["matches"]:
        results.append({
            "id": match["id"],
            "score": match["score"]
        })
    print(results)
    # return json.dumps(results)
    return json.dumps(all_data)

class MichaelScottPackageManager(Resource):
    '''
    Returns a list of all relevant packages in the Michael Scott package manager.
    '''
    # @marshal_with(workflow_fields)
    def get(self):
        
        parser = reqparse.RequestParser()
        
        parser.add_argument('keywords', type=str, required=True, help='requirements is required')
        args = parser.parse_args()
        
        # agent = DnDUtilityAgentSingleton(stream=True)
        
        packages = search_relevant_terms(args['keywords'])
        
        return {
            'packages': packages
        }

class AgentFactory(Resource):
    def post(self):
        instance = AzureModelRuntimeSingleton()
        
        parser = reqparse.RequestParser()
        
        parser.add_argument('requirements', type=list, required=True, help='requirements is required')
        args = parser.parse_args()
        
        requirements = args['requirements']
            
        messages = [
        {
            'role': 'system',
            'content': PLANNING_SYSTEM.format(requirements=requirements)
        },
        {
            'role': 'user',
            'content': PLANNING_USER.format(requirements=requirements)
        }
        ]
        
        plan = instance.run(messages=messages)
        
        keywords = plan.split('-----')[1] # TODO: Decide how to split this
        print('KEYWORDS:', keywords)
        
        with requests.Session() as session:
            data = {
                'keywords': str(keywords)
            }
            test = session.post('http://localhost:5000/miniapps/michael_scott_package_manager', json=data)
            print(test.json())
        
        relevant_packages = ''
        with requests.Session() as session:
            data = {
                'keywords': keywords
            }
            relevant_packages = workflows
        print('RELEVANT PACKAGES:', relevant_packages)
        final_output = ''
        
        messages = [
        {
            'role': 'system',
            'content': FINAL_OUTPUT_SYSTEM
        },
        {
            'role': 'user', #
            'content': FINAL_OUTPUT_USER.format(requirements=requirements, keywords=keywords, packages=relevant_packages)
        }
        ]
        
        final_output = instance.run(messages=messages) # delete last commit in git : 
        
        data = json.loads(final_output)
        print('DATA:')
        print(data)
        data['user_id'] = '1'
        with requests.session() as s:
            r = s.post('http://localhost:5000/miniapps/workflow', json=data)
        print(r.text)
        
        return {'workflow_id': r.json().get('workflow_id'),
                'workflow': data,
                'inputs': data.get('graph').get('nodes')[0].get('data').get('variables')}
        

api.add_resource(MichaelScottPackageManager, '/michael_scott_package_manager')
api.add_resource(AgentFactory, '/agent_factory')


def search_relevant_terms_from_keywords(keyword):
    import json
    import os

    import requests

    # Azure OpenAI setup
    api_base = "https://nextpy-gpt4.openai.azure.com/"
    # api_key = "*"  # Replace with your OpenAI API key
    deployment_id = "gpt-omni"  # Add your deployment ID here
    api_version = "2024-02-15-preview"

    # Azure AI Search setup
    search_endpoint = "https://agentpackagesearch783656841527.search.windows.net"  # Add your Azure AI Search endpoint here
    # search_key = "*"  # Replace with your Azure AI Search admin key
    search_index_name = "subagent-vector-1720327816935"  # Add your Azure AI Search index name here

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Define the payload
    data = {
        "data_sources": [
    {
      "type": "azure_search",
      "parameters": {
        "endpoint": search_endpoint,
        "index_name": search_index_name,
        "semantic_configuration": "subagent-vector-1720327816935-semantic-configuration",
        "query_type": "semantic",
        "fields_mapping": {},
        "in_scope": True,
        "role_information": "you are a search agent and you just give the package  name as output based on retrieved documents no additional text  if no relevant things found retrun none . use your judgement to see if the packages are relevant to user query \\n\\nexamples\\n\\nprompt - help me find a package for image\\nyour response - image_generator\\n\\nprompt - help me find a package for cat\\nyour response - none",
        "filter": True,
        "strictness": 3,
        "top_n_documents": 5,
        "authentication": {
          "type": "api_key",
          "key": "LHuY3WYl83LQFAT0EDjoHiXtFjsNORMI7DNlU19Ej2AzSeCWvNTA"
        },
        "key": "LHuY3WYl83LQFAT0EDjoHiXtFjsNORMI7DNlU19Ej2AzSeCWvNTA",
        "indexName": "subagent-vector-1720327816935"
      }
    }
  ],
  "messages": [
    {
      "role": "system",
      "content": f"you are a search agent and you just give the package  name as output based on retrieved documents no additional text  if no relevant things found retrun none . use your judgement to see if the packages are relevant to user query \\n\\nexamples\\n\\nprompt - help me find a package for image\\nyour response - image_generator\\n\\nprompt - help me find a package for {keyword}\\nyour response - none"
    }
  ],

        "messages": [
            {
                "role": "system",
                "content": ("you are a search agent and you just give the package name as output based on retrieved documents "
                            "no additional text if no relevant things found return none. Use your judgement to see if the packages "
                            "are relevant to user query\n\nexamples\n\nprompt - help me find a package for image\nyour response - image_generator\n\n"
                            "prompt - help me find a package for cat\nyour response - none")
            }
        ],
        "deployment": deployment_id,
        "temperature": 0,
        "top_p": 1,
        "max_tokens": 800,
        "stop": None,
        "stream": False
    }

    # Send the POST request
    response = requests.post(
        f"{api_base}openai/deployments/{deployment_id}/extensions/chat/completions?api-version={api_version}",
        headers=headers,
        data=json.dumps(data)
    )

    # Print the response
    print(response.json())
    
    
workflows = '''{
    "workflow_id": "123",
    "workflow_name": "Content Generator",
    "description": "Generates a short content based on the input text",
    "user_id": "1",
    "graph": {
        "nodes": [
            {
                "id": "1",
                "type": "custom",
                "data": {
                    "type": "start",
                    "title": "Start",
                    "desc": "",
                    "variables": [
                        {
                            "variable": "text",
                            "type": "text-input",
                            "required": true
                        }
                    ]
                }
            },
            {
                "id": "2",
                "data": {
                    "type": "llm",
                    "title": "Generate Short Content",
                    "desc": "Generates a short content based on the input text",
                    "system": "You are a concise and creative assistant.",
                    "user": "Create a short and engaging content based on the following input: {text}",
                    "assistant": "",
                    "output_key": "short_content"
                }
            }
        ],
        "edges": [
            {
                "source": "1",
                "target": "2",
                "data": {
                    "sourceType": "start",
                    "targetType": "llm"
                }
            }
        ]
    },
    "output_keys": ["short_content"]
}
{
    "workflow_id": "456",
    "user_id": "1",
    "workflow_name": "Image Generator",
    "description": "Generates a image based on the input text",
    "graph": {
        "nodes": [
            {
                "id": "1",
                "type": "custom",
                "data": {
                    "type": "start",
                    "title": "Start",
                    "desc": "",
                    "variables": [
                        {
                            "variable": "text",
                            "type": "text-input",
                            "required": true
                        }
                    ]
                }
            },
            {
                "id": "2",
                "data": {
                    "type": "image-gen",
                    "title": "IMAGE_GEN",
                    "desc": "",
                    "prompt": "{text}",
                    "output_key": "image_url"
                }
            }
        ],
        "edges": [
            {
                "source": "1",
                "target": "2",
                "data": {
                    "sourceType": "start",
                    "targetType": "image-gen"
                }
            }
        ]
    },
    "output_keys": ["image_url"]
}

{
    "workflow_id": "789",
    "user_id": "1",
    "workflow_name": "Website Generator",
    "description": "Generates a short html webpage based on the input text and image url",
    "graph": {
        "nodes": [
            {
                "id": "1",
                "type": "custom",
                "data": {
                    "type": "start",
                    "title": "Start",
                    "desc": "",
                    "variables": [
                        {
                            "variable": "text",
                            "type": "text-input",
                            "required": true
                        },
                        {
                            "variable": "image_url",
                            "type": "text-input",
                            "required": true
                        }
                    ]
                }
            },
            {
                "id": "2",
                "data": {
                    "type": "llm",
                    "title": "LLM",
                    "desc": "",
                    "system": "You are a helpful AI assistant.",
                    "user": "Create html code following the instructions: {text} do not enclose it in codeblocks, incorporate the following images: {image_url}",
                    "assistant": "",
                    "output_key": "html"
                }
            }
        ],
        "edges": [
            {
                "source": "1",
                "target": "2",
                "data": {
                    "sourceType": "start",
                    "targetType": "llm"
                }
            }
        ]
    },
    "output_keys": ["html"]
}

Example of workflow that cam combine different flows:
data={
        'workflow_id': '123',
        'user_id': '1',
        'graph': {
    "nodes": [
        {
            "id": "1",
            "data": {
                "type": "start",
                "title": "Start",
                "desc": "",
                "variables": [
                    {
                        "variable": "query",
                        "required": True
                    },
                    {
                        "variable": "style",
                        "required": True
                    }
                ]
            },
        },
        {
            "id": "2",
            "data": {
                "type": "llm",
                "title": "LLM",
                "desc": "Generate a description for the query",
                "variables": [],
                "system": "You are a helpful AI assistant.",
                "user": "You are tasked with writing a blog post for the given topic: {query}, in the writing style {style}",
                "assistant": "",
                "output_key": "image_desc",
            }
        },
        {
            "id": "3",
            "data": {
                "type": "workflow",
                "title": "SUBFLOW",
                "desc": "Generate images from the llm output generated by node 2",
                "workflow_id": "456",
                "inputs": {
                    "text": "{image_desc}"
                },
                "output_key": "image_url"
            }
        },
        {
            "id": "4",
            "data": {
                "type": "workflow",
                "title": "SUBFLOW",
                "desc": "Generate html article from the llm output and image url",
                "workflow_id": "789",
                "inputs": {
                    "text": "{image_desc}",
                    "image_url": "{image_url}"
                },
                "output_key": "html"
            }
        }
    ],
    "edges": [
        {
            "id": "1",
            "source": "1",
            "target": "2",
            "data": {
                "sourceType": "start",
                "targetType": "llm"
            }
        },
        {
            "id": "2",
            "source": "2",
            "target": "3",
            "data": {
                "sourceType": "llm",
                "targetType": "workflow"
            }
        },
        {
            "id": "3",
            "source": "3",
            "target": "4",
            "data": {
                "sourceType": "workflow",
                "targetType": "workflow"
            }
        }
    ],
},
    "output_keys": ["html"]
    
    }

'''