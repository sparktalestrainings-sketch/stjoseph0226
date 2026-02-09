def detect_intent(text):
    text = text.lower()
    if "fee" in text or "payment" in text:
        return "finance"
    if "register" in text or "course" in text:
        return "academic"
    if "admission" in text or "apply" in text:
        return "admissions"
    if "wifi" in text or "login" in text:
        return "it"
    return "general"
