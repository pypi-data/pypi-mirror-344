# ai_snake/parser.py

def parse_code(code):
    """
    Very basic parser: just splits code into lines.
    """
    return code.strip().split('\n')