import asyncio
import copy
import ctypes
import json
import logging
from typing import Any, Dict, Union

import nest_asyncio
from core.miniapps.dnd.config import Config
from core.miniapps.dnd.dnd_agent.utils import _llm_from_template
from nextpy.ai import engine
from nextpy.ai.agent.base_agent import BaseAgent
from nextpy.ai.engine import Program
from nextpy.ai.engine._program import extract_text


class DnDAgent(BaseAgent):

    def __init__(self, system_prompt,
                 player_name,
                 player_class,
                 player_race,
                 player_area,
                 player_attributes,
                 llm=None, memory=None, async_mode=False, stream=False, **kwargs):
        super().__init__(llm=llm, **kwargs)
        if llm is None:
            llm = engine.llms.OpenAI(model='gpt-3.5-turbo-16k')
        self.system_prompt = system_prompt
        self.player_name = player_name
        self.player_class = player_class
        self.player_race = player_race
        self.player_attributes = player_attributes
        self.player_area = player_area
        self.engine: Program = _llm_from_template(llm=llm, file_name='dnd', memory=memory, async_mode=async_mode, stream=stream)
        self.return_complete = True

    def agent_type(self):
        return "chat"

    def get_all_classes(self):
        return '\n'.join([f'{unique_class.name} - {unique_class.description}' for unique_class in self.all_classes])

    def get_all_races(self):
        return '\n'.join([f'{unique_race.name} - {unique_race.description}' for unique_race in self.all_races])

    def get_all_areas(self):
        return '\n'.join([f'{unique_area.name} - {unique_area.description}' for unique_area in self.all_races])

    def run(self, **kwargs):
        if len(self._memory_related_tasks) > 0:
            try:
                other_loop = asyncio.get_event_loop()
                nest_asyncio.apply(other_loop)
            except RuntimeError:
                pass
            loop = asyncio.new_event_loop()
            for task in self._memory_related_tasks[:]:
                if not task.done():
                    # print('\n\nFound a memory related task that is not yet done, calling loop.run_until_complete..\n\n')
                    loop.run_until_complete(task)
                self._memory_related_tasks.remove(task)
        _knowledge_variable = self.get_knowledge_variable

        if _knowledge_variable:
            if kwargs.get(_knowledge_variable):
                query = kwargs.get(_knowledge_variable)
                retrieved_knowledge = self.get_knowledge(query)
                output = self.engine(
                    RETRIEVED_KNOWLEDGE=retrieved_knowledge, **kwargs, silent=True
                )
            else:
                raise ValueError("knowledge_variable not found in input kwargs")
        else:
            output = self.engine(dungeon_master_info=self.system_prompt,
                                         player_name=self.player_name,
                                         player_class=self.player_class,
                                         player_race=self.player_race,
                                         player_attributes=self.player_attributes,
                                         player_area=self.player_area,
                                         **kwargs, silent=True, from_agent=True)

            # Handle memory here
            if self.engine.memory is not None:
                self._handle_memory(output)

        if self.return_complete:
            return output

        _output_key = (
            self.output_key
            if self.output_key is not None
            else self.get_output_key(output)
        )

        if output.variables().get(_output_key):
            return output[_output_key]
        else:
            logging.warning("Output key not found in output, so full output returned")
            return output

    async def arun(self, **kwargs) -> Union[str, Dict[str, Any]]:
        """Async method to Run the agent to generate a response to the user query."""

        # Check if any pending memory related tasks left, we have control of event loop so do them now
        if len(self._memory_related_tasks) > 0:
            for task in self._memory_related_tasks[:]:
                if not task.done():
                    # print('\n\nFound a memory related task that is not yet done, awaiting it now..\n\n')
                    await task
                self._memory_related_tasks.remove(task)

        _knowledge_variable = self.get_knowledge_variable

        if _knowledge_variable:
            if kwargs.get(_knowledge_variable):
                query = kwargs.get(_knowledge_variable)
                retrieved_knowledge = self.get_knowledge(query)
                output = self.engine(
                    RETRIEVED_KNOWLEDGE=retrieved_knowledge, **kwargs, silent=True
                )
            else:
                raise ValueError("knowledge_variable not found in input kwargs")
        else:
            # print('Calling compiler..')
            output = await self.engine(dungeon_master_info=self.system_prompt,
                                         player_name=self.player_name,
                                         player_class=self.player_class,
                                         player_race=self.player_race,
                                         player_attributes=self.player_attributes,
                                         current_area=f'Area name: {self.current_area}\n'
                                                      f'Area description {self.current_area}',
                                         dnd_agent=id(self),
                                         tool=self.tools,
                                         tool_func=tool_use,
                                         **kwargs, silent=True, from_agent=True)
            print(output.__str__()[:300])
            # print('Finished compiler call..')
            # Add new memory to ConversationHistory
            # print(f'self.compiler.memory : {self.compiler.memory}')
            # if self.compiler.memory is not None:
                # print('Found memory, calling self._handle_memory()')
                # self._handle_memory(output)
            print('')
        if self.return_complete:
            return output

        _output_key = (
            self.output_key
            if self.output_key is not None
            else self.get_output_key(output)
        )

        if output.variables().get(_output_key):
            return output[_output_key]
        else:
            logging.warning("Output key not found in output, so full output returned")
            return output

    def _handle_memory(self, new_program):
        # print('In handle memory')
        if self.engine.async_mode:
            # print('Async mode is true')
            loop = asyncio.get_event_loop()
            assert loop.is_running(), "The program is in async mode but there is no asyncio event loop running! Start one and try again."
            scheduled_task = loop.create_task(self._update_memory(new_program))
            # print('Scheduled update memory')
            self._memory_related_tasks.append(scheduled_task)
        else:
            try:
                other_loop = asyncio.get_event_loop()
                import nest_asyncio
                nest_asyncio.apply(other_loop)
            except RuntimeError:
                pass
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._update_memory(new_program))

    async def _update_memory(self, new_program):
        # print('\nIn update memory..\n')
        all_text = extract_text(new_program.text)
        if asyncio.iscoroutine(self.engine.memory.add_memory):
            for text_block in all_text:
                for value in text_block:
                    await self.engine.memory.add_memory(prompt=value, llm_response=text_block[value])
        else:
            for text_block in all_text:
                for value in text_block:
                    # print(f'adding user : {value} llm_response: {text_block[value]} to memory')
                    self.engine.memory.add_memory(prompt=value, llm_response=text_block[value])
        # print(f'Current memory prompts : {self.engine.memory.memory_prompts}')

        if asyncio.iscoroutine(self.engine.memory.get_memory):
            self.engine.ConversationHistory = await self.engine.memory.get_memory()
        else:
            self.engine.ConversationHistory = self.engine.memory.get_memory()
        # print(f'\nUpdated memory successfully!\nCurrent ConvHistory: {self.engine.ConversationHistory}\n\n')


def tool_use(var: dict):
    var = json.loads(var)
    print('VAR:', var)
    dnd_agent: DnDAgent = ctypes.cast(var['dnd_agent'], ctypes.py_object).value
    tools = (dnd_agent.get_all_classes, dnd_agent.get_all_races, dnd_agent.get_all_areas)
    return tools[int(var['index'])]()


class CharacterClass:
    def __init__(self, group):
        self.name = group[0]
        self.emoji = group[1]
        self.description = group[2]

    def to_dict(self):
        return {'name': self.name, 'emoji': self.emoji, 'description': self.description}

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
        
        else:
            instance = copy.copy(cls._instances[settings])
            instance.__dict__.update(kwargs)
            return instance
        

class DnDAgentSingleton(DnDAgent, metaclass=UtilityMeta):
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
