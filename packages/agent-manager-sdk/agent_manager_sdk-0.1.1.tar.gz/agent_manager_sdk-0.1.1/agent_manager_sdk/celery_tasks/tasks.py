from celery import shared_task

from ..app_extensions.db_ext import db
from ..core.miniapps.dnd.prompts import (
    SUMMARIZER_SYSTEM,
    SUMMARIZER_USER,
)
from ..core.model_runtimes.openai.azure import AzureModelRuntimeSingleton
from ..models.miniapps.dnd import Chat
from ..utils.miniapps.dnd import _combine_histories


def _generate_messages(system, user):
    return [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user}
    ]

@shared_task(ignore_result=True)
def summarize_chat(user_id: int) -> None:
    chat = db.session.query(Chat).filter_by(user_id=user_id).first()
    
    ai_history = chat.ai_history if chat.ai_history else []
    user_history = chat.user_history if chat.user_history else []
    
    summaries = chat.summaries if chat.summaries else []
    
    
    instance = AzureModelRuntimeSingleton()
    
    ai_history = ai_history[len(summaries)*10:len(summaries)*10+1] # 10 messages per summary
    user_history = user_history[len(summaries)*10:len(summaries)*10+1] # 10 messages per summary
    
    history = _combine_histories(ai_history, user_history, summaries)
    # 2 messages per summary
    # ai_history = ai_history[len(summaries)*2:len(summaries)*2+2]
    # user_history = user_history[len(summaries)*2:len(summaries)*2+2]
    
    summary = instance.run(messages=_generate_messages(SUMMARIZER_SYSTEM, SUMMARIZER_USER.format(conversation_history=history)))
    
    print(summary)
    
    chat.summaries = summaries + [summary]
    
    db.session.commit()
          
    return summary