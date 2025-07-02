import re


def get_is_spam(text: str) -> bool:
    """ Check if text is spam

    Args:
        text (str): text to check

    Returns:
        bool: true if text is spam
    """
    
    # Mask as spam empty messages
    if not text:
        return True

    regexs = [
        # links
        r"(https?://[^\s]+)",

        # amount + usd
        r"(\d+[\.,]?\d*)\s*(?:USD|usd)",

        # $ + amount
        # r"\$(\d+[\.,]?\d*)",

        # special words
        r"(more\s*info|our\s*plans|seo|contact\s*us|discord|roi)",
        r"(convertible\s*debtfinancing|repayment|marketing)"

        # percentaje
        r"(\d+[\.,]?\d*)\s*%",
    ]

    # Merge all regexs
    regex = "|".join(regexs)

    # Validate regex in each text
    regex_found = re.search(regex, text, re.IGNORECASE)
    if regex_found:
        return True
    else:
        return False


def get_message_subject(inputs: dict) -> str:
    """ Get message formatted from inputs

    Args:
        inputs (dict): inputs from form

    Returns:
        str: message formatted
    """
    message = ""
    subject = "New contact message!"
    for input_name, input_value in inputs.items():
        
        # Skip unrelated fields
        if "file" in input_name:
            continue

        # Get custom subject
        if input_name == "subject":
            subject = input_value
            
        # Get body values
        skip_fields = [
            # User field
            "api_key",
            "redirect",
            "subject",
            "user",
            # Django field
            "csrfmiddlewaretoken",
            # wordpress fields
            "et_pb_",
            "_wp",
            "token",
        ]
        skip = False
        for skip_field in skip_fields:
            if skip_field in input_name:
                skip = True
                break
        if skip:
            continue
        message += f"{input_name}: {input_value}\n"

    return message, subject
