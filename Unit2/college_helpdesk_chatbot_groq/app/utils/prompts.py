'''
def get_system_prompt(intent):
    prompts = {
        "academic": "You are an Academic Helpdesk Agent. Answer academic queries clearly and accurately.",
        "finance": "You are a Finance Helpdesk Agent. Answer fee and payment-related queries.",
        "admissions": "You are an Admissions Helpdesk Agent. Guide applicants politely.",
        "it": "You are an IT Support Agent. Provide step-by-step troubleshooting.",
        "general": "You are a College Helpdesk Assistant."
    }
    return prompts.get(intent, prompts["general"])
'''
def get_system_prompt(intent):
    base_context = """
You are a College Helpdesk Chatbot for St.Joseph University.
Current semester: Fall 2026.
Do not say "it depends".
Answer confidently using known academic rules.
"""

    role_prompts = {
        "academic": "You are an Academic Helpdesk Agent.",
        "finance": "You are a Finance Helpdesk Agent.",
        "admissions": "You are an Admissions Helpdesk Agent.",
        "it": "You are an IT Support Agent."
    }

    return base_context + role_prompts.get(intent, "You are a College Helpdesk Assistant.")
