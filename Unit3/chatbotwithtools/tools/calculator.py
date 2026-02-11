def calculate(expression: str):
    try:
        # WARNING: eval is used only for training/demo purposes
        result = eval(expression)
        return f"🧮 Result: {result}"
    except Exception:
        return "❌ Invalid mathematical expression"
