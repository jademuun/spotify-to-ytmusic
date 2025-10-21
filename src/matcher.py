from rapidfuzz import fuzz

def good_title_match(a: str, b: str, threshold: int = 85) -> bool:
    return fuzz.token_set_ratio(a or "", b or "") >= threshold
