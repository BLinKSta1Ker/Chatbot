import bleach

def sanitize_input(user_input):
    """Sanitizes user input to remove harmful content."""
    allowed_tags = []
    return bleach.clean(user_input, tags=allowed_tags, strip=True)