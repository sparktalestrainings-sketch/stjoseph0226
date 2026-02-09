'''
def init_memory():
    return {
        "intent_history": [],
        "last_query": ""
    }

def update_memory(memory, intent, query):
    memory["intent_history"].append(intent)
    memory["last_query"] = query



“The memory.py module implements multi-turn dialogue by maintaining session-level context. 
It stores the user’s intent history and last query using a lightweight dictionary.
This memory is injected into each LLM prompt, allowing the chatbot to generate 
context-aware responses across multiple conversation turns.”
'''
def init_memory():
    return {
        "active_intent": None,
        "intent_history": [],
        "last_query": ""
    }

def update_memory(memory, intent, query):
    memory["intent_history"].append(intent)
    memory["last_query"] = query
    memory["active_intent"] = intent
