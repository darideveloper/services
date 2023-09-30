import re

def is_spam (text:str) -> bool:
    """ Check if text is spam 
    
    Args:
        text (str): text to check
        
    Returns:
        bool: true if text is spam
    """

    regexs = [
        # links
        r"(https?://[^\s]+)",
        
        # amount + usd
        r"(\d+[\.,]?\d*)\s*(?:USD|usd)",
        
        # $ + amount
        r"\$(\d+[\.,]?\d*)",
        
        # special words
        r"(more\s*info|our\s*plans|seo|contact\s*us|discord|roi|convertible\s*debt|loan\s*financing|early\s*repayment\s*penalties|content\s*marketing|humanly\s*written\s*seo\s*content)",
        
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