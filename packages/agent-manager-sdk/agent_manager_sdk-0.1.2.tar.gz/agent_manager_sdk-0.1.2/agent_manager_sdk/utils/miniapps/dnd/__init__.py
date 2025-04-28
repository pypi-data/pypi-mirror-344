
def _combine_histories(ai_history, user_history, summaries=None):    
    if summaries:
            ai_history = ai_history[len(summaries)*10:] # 10 messages per summary
            user_history = user_history[len(summaries)*10:] # 10 messages per summary
    history = _get_chat_history(ai_history, user_history)
    combined_history = '\n'.join([f"{item['type'].capitalize()}: {item['message']}" for item in history])
    
    for summary in summaries:
        combined_history += f"Prior events: {summary}"
    print('Returning combined history', combined_history)
    return combined_history        
    
def _get_chat_history(ai_history, user_history):
    chat_history = []
    
    for i in range(max(len(ai_history), len(user_history))):
        if i < len(ai_history):
            chat_history.append({'type':'ai',
                                 'message': ai_history[i]})
        if i < len(user_history):
            chat_history.append({'type':'user',
                                 'message': user_history[i]})
    
    return chat_history

def validate_workflow(workflow_json):
    """Validate a workflow structure"""
    graph = workflow_json.get("graph", {})
    nodes = graph.get("nodes", [])
    if not nodes:
        raise ValueError("Workflow must have at least one node.")
    for node in nodes:
        if "data" not in node or "type" not in node["data"]:
            raise ValueError("Node missing required 'type' field")