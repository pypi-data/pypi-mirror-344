import logging
from pathlib import Path
from typing import Any, Dict, Union

from core.miniapps.dnd.config import Config
from dotenv import load_dotenv
from nextpy.ai import engine
from nextpy.ai.agent.base_agent import BaseAgent


class SummarizeAgent(BaseAgent):
    def __init__(self, llm=None, memory=None, async_mode=False, stream=False, **kwargs):
        super().__init__(llm=llm, **kwargs)
        if llm is None:
            llm = engine.llms.OpenAI(model='gpt-3.5-turbo-16k')
        
        self.summarize_agent = _llm_from_template(llm=llm, file_name='summarize', memory=memory, async_mode=async_mode, stream=stream)
        self.return_complete = True
    
    def agent_type(self):
        return "chat"
    
    def run(self, gen_type: str, **kwargs) -> Union[str, Dict[str, Any]]:
        """Run the agent to generate a response to the user query."""
        
        _knowledge_variable = self.get_knowledge_variable
        
        if _knowledge_variable:
            if kwargs.get(_knowledge_variable):
                query = kwargs.get(_knowledge_variable)
                retrieved_knowledge = self.get_knowledge(query)
                output = self.engine(RETRIEVED_KNOWLEDGE=retrieved_knowledge, **kwargs, silent=True)
            else:
                raise ValueError("knowledge_variable not found in input kwargs")
        else:
            if gen_type.lower() == 'summarize':
                output = self.summarize_agent(**kwargs)
            else:
                output = self.engine(**kwargs)
        if self.return_complete:
            return output
        _output_key = self.output_key if self.output_key is not None else self.get_output_key(output)
        
        if output.variables().get(_output_key):
            return output[_output_key]
        else:
            logging.warning("Output key not found in output, so full output returned")
            return output

class DnDUtilityAgent(BaseAgent):

    def __init__(self, llm=None, memory=None, async_mode=False, stream=False, **kwargs):
        super().__init__(llm=llm, **kwargs)
        if llm is None:
            llm = engine.llms.OpenAI(model='gpt-3.5-turbo-16k')

        self.theme_agent = _llm_from_template(llm=llm, file_name='theme', memory=memory, async_mode=async_mode, stream=stream)
        self.class_agent = _llm_from_template(llm=llm, file_name='class', memory=memory, async_mode=async_mode, stream=stream)
        self.character_agent = _llm_from_template(llm=llm, file_name='character', memory=memory, async_mode=async_mode, stream=stream)
        self.return_complete = True
    def agent_type(self):
        return "chat"

    def run(self, gen_type: str, **kwargs) -> Union[str, Dict[str, Any]]:
        """Run the agent to generate a response to the user query."""

        _knowledge_variable = self.get_knowledge_variable

        if _knowledge_variable:
            if kwargs.get(_knowledge_variable):
                query = kwargs.get(_knowledge_variable)
                retrieved_knowledge = self.get_knowledge(query)
                output = self.engine(RETRIEVED_KNOWLEDGE=retrieved_knowledge, **kwargs, silent=True)
            else:
                raise ValueError("knowledge_variable not found in input kwargs")
        else:
            if gen_type.lower() == 'description':
                output = self.theme_agent(**kwargs)
            elif gen_type.lower() == 'class':
                output = self.class_agent(**kwargs)
            elif gen_type.lower() == 'character':
                output = self.character_agent(**kwargs)
            else:
                output = self.engine(**kwargs)
        if self.return_complete:
            return output
        _output_key = self.output_key if self.output_key is not None else self.get_output_key(output)

        if output.variables().get(_output_key):
            return output[_output_key]
        else:
            logging.warning("Output key not found in output, so full output returned")
            return output



load_dotenv('secrets/secrets.env')

def _llm_from_template(llm, file_name, memory, **kwargs):
    template = _get_template(file_name)
    print(template)
    client = engine(template=template, llm=llm, memory=memory, **kwargs)
    return client


def _get_template(file_name):
    try:
        # .hbs files are stored in parent/templates
        parent = Path(__file__).parent.parent
        return Path(f'{parent}/templates/{file_name}.hbs').read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError('NOTE : Store your templates in ./templates as .hbs files.')
    
class UtilityMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        settings = ''
        stream = f'stream_{kwargs.get("stream", False)}'
        async_mode = f'async_{kwargs.get("async_mode", False)}'
        settings = f'{stream}_{async_mode}'
        
        if settings not in cls._instances:
            llm = _generate_llm()
            kwargs['llm'] = llm
            instance = super().__call__(*args, **kwargs)
            cls._instances[settings] = instance
        return cls._instances[settings]

class DnDUtilityAgentSingleton(DnDUtilityAgent, metaclass=UtilityMeta):
    def __init__(self, async_mode=False, stream=False, **kwargs):
        super().__init__(async_mode=async_mode, stream=stream, **kwargs)       
        
class SummarizeAgentSingleton(SummarizeAgent, metaclass=UtilityMeta):
    def __init__(self, async_mode=False, stream=False, **kwargs):
        super().__init__(async_mode=async_mode, stream=stream, **kwargs)
        
def _generate_llm():
    return engine.llms.OpenAI(
            model=Config.OPENAI_MODEL,
            api_type=Config.OPENAI_API_TYPE,
            api_key=Config.OPENAI_API_KEY,
            api_base=Config.OPENAI_API_BASE,
            api_version=Config.OPENAI_API_VERSION,
            deployment_id=Config.OPENAI_DEPLOYMENT_ID,
            caching=False,
        )
