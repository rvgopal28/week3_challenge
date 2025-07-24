def is_uncertain(text):
    uncertainty_triggers = ["not sure", "maybe", "don't know", "unclear", "let me check"]
    return any(trigger in text.lower() for trigger in uncertainty_triggers)