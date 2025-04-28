import json
import threading

from flask import Response, stream_with_context
from flask_restful import Resource, reqparse

from .....app_extensions.db_ext import db
from .....celery_tasks.tasks import summarize_chat
from .....controllers.console import api
from .....core.miniapps.dnd.prompts import (
    _CLASS_BASE,
    CHARACTER_SYSTEM,
    CHARACTER_USER,
    CLASS_AREAS_USER,
    CLASS_CLASS_USER,
    CLASS_NAME_USER,
    CLASS_SYSTEM,
    DND_SYSTEM,
    DND_USER,
    SUMMARIZER_SYSTEM,
    SUMMARIZER_USER,
    THEME_DESCRIPTION_USER,
    THEME_SYSTEM,
    THEME_TITLE_USER,
    ClASS_RACE_USER,
)
from .....core.model_runtimes.openai.azure import AzureModelRuntimeSingleton
from .....models.miniapps.dnd import Chat, User
from .....utils.miniapps.dnd import _combine_histories, _get_chat_history


def _generate_messages(system, user):
    return [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user}
    ]

class GenerateMasterPromptAPI(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('theme', type=str, required=True, help='Theme is required')
        args = parser.parse_args()
        
        # agent = DnDUtilityAgentSingleton(stream=True)
        instance = AzureModelRuntimeSingleton()
        
        def stream_result():
            messages = _generate_messages(THEME_SYSTEM, THEME_DESCRIPTION_USER.format(theme=args['theme']))
            
            description = ''
            
            for result in instance.sync_stream(messages=messages):
                yield json.dumps({
                    'title': '',
                    'description': result
                }) + '\n'
                description = result
            
            messages[1]['content'] = THEME_TITLE_USER.format(description=result)
            
            for result in instance.sync_stream(messages=messages):
                yield json.dumps({
                    'title': result,
                    'description': description
                }) + '\n'
            
        return Response(stream_with_context(stream_result()), mimetype='application/json')
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str, required=True, help='Description is required')
        args = parser.parse_args()
        
        user = User.query.get(args['user_id'])
        
        if user is None:
            db.session.add(User(id=args['user_id']))
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        if chat:
            chat.description = args['description']
            chat.ai_history = None
            chat.user_history = None
        else:
            db.session.add(Chat(user_id=args['user_id'], title=args['title'], description=args['description']))

        # clear history
        
        
        db.session.commit()
        
        return 'Success', 200
                

class GenerateClassAPI(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('theme', type=str, required=True, help='Theme is required')
        args = parser.parse_args()
        
        instance = AzureModelRuntimeSingleton()
        
        class_messages = _generate_messages(CLASS_SYSTEM, CLASS_CLASS_USER.format(theme=args['theme']))
        name_messages = _generate_messages(CLASS_SYSTEM, CLASS_NAME_USER.format(theme=args['theme']))
        race_messages = _generate_messages(CLASS_SYSTEM, ClASS_RACE_USER.format(theme=args['theme']))
        area_messages = _generate_messages(CLASS_SYSTEM, CLASS_AREAS_USER.format(theme=args['theme']))
        
        responses = {}
        
        def run_instance(messages):
            response = instance.run(messages=messages)
            try:
                response = json.loads(response)
            except TypeError as e:
                print(f'For messages : {messages}, got type error: {e}')
            responses.update(response)
        
        threads = []
        for messages in [class_messages, name_messages, race_messages, area_messages]:
            thread = threading.Thread(target=run_instance, args=(messages,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        return responses
        
    
    def post(self):
        parser = reqparse.RequestParser()
        
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        parser.add_argument('class', type=str, required=True, help='Class is required')
        parser.add_argument('race', type=str, required=True, help='Race is required')
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('area', type=str, required=True, help='Area is required')
        args = parser.parse_args()
        
        print(f'Received request with args: {args}')
        
        
        user = User.query.get(args['user_id'])
        
        if user is None:
            db.session.add(User(id=args['user_id']))
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        if chat:
            chat.player_class = args['class']
            chat.player_race = args['race']
            chat.player_name = args['name']
            chat.player_area = args['area']
            chat.ai_history = None
            chat.user_history = None
        else:
            db.session.add(Chat(user_id=args['user_id'], player_class=args['player_class'], player_race=args['player_race'], player_name=args['player_name'], player_area=args['player_area']))
        
        
        db.session.commit()
        
        return "Success", 200

class GenerateAttributesAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='User ID is required')
        
        args = parser.parse_args()
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        instance = AzureModelRuntimeSingleton()
        
        messages = _generate_messages(CHARACTER_SYSTEM, CHARACTER_USER.format(player_class=chat.player_class, 
                                                                              player_race=chat.player_race,
                                                                              player_name=chat.player_name))
        
        response = instance.run(messages=messages)
        
        chat.player_attributes = response
        db.session.commit()
        
        return {
            'attributes': json.loads(response)
            }

class StartGameAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        args = parser.parse_args()
                
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        ai_history = []
        

        instance = AzureModelRuntimeSingleton()
        
        meta_information = "Let's start the game with the first event."
        
        def stream_result():
            messages = _generate_messages(DND_SYSTEM.format(dungeon_master_info=chat.description,
                                                            player_name=chat.player_name,
                                                            player_class=chat.player_class,
                                                            player_race=chat.player_race,
                                                            player_attributes=chat.player_attributes,
                                                            player_area=chat.player_area),
                                          DND_USER.format(meta_information=meta_information,
                                                          conversation_history=ai_history)
                                          )

            for response in instance.sync_stream(messages=messages):
                yield json.dumps({
                    'response': response
                }) + '\n'
            
            
        
            chat.ai_history = ai_history + [response]
        
            db.session.commit()
        
        return Response(stream_with_context(stream_result()), mimetype='application/json')
        
class UnstreamedStartGameAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        args = parser.parse_args()
                
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        ai_history = []
        
        instance = AzureModelRuntimeSingleton()
        meta_information = "Let's start the game with the first event."
        
        messages = _generate_messages(DND_SYSTEM.format(dungeon_master_info=chat.description,
                                                            player_name=chat.player_name,
                                                            player_class=chat.player_class,
                                                            player_race=chat.player_race,
                                                            player_attributes=chat.player_attributes,
                                                            player_area=chat.player_area),
                                          DND_USER.format(meta_information=meta_information,
                                                          conversation_history=ai_history)
                                          )
        response = instance.run(messages=messages)
        
                                                                              
        # chat.ai_history = ai_history + [response.get('followup')]
        chat.ai_history = ai_history + [response]
        
        db.session.commit()
        
        return {
            'response': response
        }
        



class PerformActionAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        parser.add_argument('action', type=str, required=True, help='action is required')
        args = parser.parse_args()
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        ai_history = chat.ai_history if chat.ai_history else []
        user_history = chat.user_history if chat.user_history else []
        summaries = chat.summaries if chat.summaries else []
        
        combined_history = _combine_histories(ai_history, user_history, summaries)        
        
        instance = AzureModelRuntimeSingleton()
        
        meta_information = f'''Generate the next event in the game based on the player's choice,
        Player chooses:
        {args.action}'''
        
        def stream_result():
            
            messages = _generate_messages(DND_SYSTEM.format(dungeon_master_info=chat.description,
                                                            player_name=chat.player_name,
                                                            player_class=chat.player_class,
                                                            player_race=chat.player_race,
                                                            player_attributes=chat.player_attributes,
                                                            player_area=chat.player_area),
                                          DND_USER.format(meta_information=meta_information,
                                                          conversation_history=combined_history)
                                          )
            
            for response in instance.sync_stream(messages=messages):
                yield json.dumps({
                    'response': response
                }) + '\n'
            
            # response = response.get('followup')
            chat.ai_history = ai_history + [response]
            chat.user_history = user_history + [args.action]
            
            db.session.commit()
            
            if len(ai_history) - (len(summaries)*10) > 10:
                print('Summarizing chat')
                summary = summarize_chat.delay(args['user_id'])
                print(summary)
        
        return Response(stream_with_context(stream_result()), mimetype='application/json')
        
class UnstreamedPerformActionAPI(Resource):
        
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        parser.add_argument('action', type=str, required=True, help='action is required')
        args = parser.parse_args()
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        ai_history = chat.ai_history if chat.ai_history else []
        user_history = chat.user_history if chat.user_history else []
        summaries = chat.summaries if chat.summaries else []
        
        combined_history = _combine_histories(ai_history, user_history, summaries)
        
        instance = AzureModelRuntimeSingleton()
        meta_information = f'''Generate the next event in the game based on the player's choice,
        Player chooses:
        {args.action}'''
        
        # response = agent.run(meta_information=meta_information,
        #                 conversation_history=combined_history)
        
        messages = _generate_messages(DND_SYSTEM.format(dungeon_master_info=chat.description,
                                                            player_name=chat.player_name,
                                                            player_class=chat.player_class,
                                                            player_race=chat.player_race,
                                                            player_attributes=chat.player_attributes,
                                                            player_area=chat.player_area),
                                          DND_USER.format(meta_information=meta_information,
                                                          conversation_history=combined_history)
                                          )
        
        response = instance.run(messages=messages)
        
        # response = response.get('followup')
        
        chat.ai_history = ai_history + [response]
        chat.user_history = user_history + [args.action]
        db.session.commit()
        
        return {
            # 'response': response.get('followup')
            'response': response
        }
            

class ContinueSceneAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        args = parser.parse_args()
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        ai_history = chat.ai_history if chat.ai_history else []
        user_history = chat.user_history if chat.user_history else []
        summaries = chat.summaries if chat.summaries else []
        
        combined_history = _combine_histories(ai_history, user_history, summaries)
        
        meta_information = '''Continue generating the last event further.'''
        instance = AzureModelRuntimeSingleton()
        
        def stream_result():
            
            messages = _generate_messages(DND_SYSTEM.format(dungeon_master_info=chat.description,
                                                            player_name=chat.player_name,
                                                            player_class=chat.player_class,
                                                            player_race=chat.player_race,
                                                            player_attributes=chat.player_attributes,
                                                            player_area=chat.player_area),
                                          DND_USER.format(meta_information=meta_information,
                                                          conversation_history=combined_history)
                                          )
            
            for response in instance.sync_stream(messages=messages):
                yield json.dumps({
                    'response': response
                }) + '\n'
                
            chat.ai_history = ai_history + [response]
            chat.user_history = user_history + ['Player choose to continue the scene']
            db.session.commit()
        
        return Response(stream_with_context(stream_result()), mimetype='application/json')

class UnstreamedContinueSceneAPI(Resource):
            
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        args = parser.parse_args()
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        ai_history = chat.ai_history if chat.ai_history else []
        user_history = chat.user_history if chat.user_history else []
        summaries = chat.summaries if chat.summaries else []
        combined_history = _combine_histories(ai_history, user_history, summaries)
        
        instance = AzureModelRuntimeSingleton()
        
        meta_information = '''Continue generating the last event further.'''
        
        messages = _generate_messages(DND_SYSTEM.format(dungeon_master_info=chat.description,
                                                            player_name=chat.player_name,
                                                            player_class=chat.player_class,
                                                            player_race=chat.player_race,
                                                            player_attributes=chat.player_attributes,
                                                            player_area=chat.player_area),
                                          DND_USER.format(meta_information=meta_information,
                                                          conversation_history=combined_history)
                                          )
        
        response = instance.run(messages=messages)
        
        chat.ai_history = ai_history + [response]
        chat.user_history = user_history + ['Player choose to continue the scene']
        db.session.commit()
        
        return {
            
            'response': response
        }
                

class FetchChatAPI(Resource):
        
        def get(self):
            parser = reqparse.RequestParser()
            
            parser.add_argument('user_id', type=str, required=True, help='user_id is required')
            args = parser.parse_args()
            
            chat = Chat.query.filter_by(user_id=args['user_id']).first()
            
            return {
                'title': chat.title,
                'description': chat.description,
                'player_class': chat.player_class,
                'player_race': chat.player_race,
                'player_name': chat.player_name,
                'player_area': chat.player_area,
                'player_attributes': chat.player_attributes,
                'chat_history': _get_chat_history(chat.ai_history, chat.user_history)
            }
            
class ResetChatAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('user_id', type=str, required=True, help='user_id is required')
        args = parser.parse_args()
        
        chat = Chat.query.filter_by(user_id=args['user_id']).first()
        
        chat.player_class = None
        chat.player_race = None
        chat.player_name = None
        chat.player_area = None
        chat.player_attributes = None
        chat.ai_history = None
        chat.user_history = None
        chat.title = None
        chat.description = None
        
        db.session.commit()
        
        return 'Success', 200
    
api.add_resource(GenerateMasterPromptAPI, '/dnd/theme')
api.add_resource(GenerateClassAPI, '/dnd/class')
api.add_resource(GenerateAttributesAPI, '/dnd/attributes')
api.add_resource(StartGameAPI, '/dnd/start')
api.add_resource(PerformActionAPI, '/dnd/action')
api.add_resource(ContinueSceneAPI, '/dnd/continue')
api.add_resource(FetchChatAPI, '/dnd/chat')
api.add_resource(ResetChatAPI, '/dnd/reset')
api.add_resource(UnstreamedStartGameAPI, '/dnd/unstreamed_start')
api.add_resource(UnstreamedPerformActionAPI, '/dnd/unstreamed_action')
api.add_resource(UnstreamedContinueSceneAPI, '/dnd/unstreamed_continue')