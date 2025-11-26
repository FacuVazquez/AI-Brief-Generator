import re
import unicodedata


def normalize(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'(.)\1+', r'\1', text)

    return text.lower().strip()


PROFANITY_LIST = [
    'fuck', 'fuk', 'fuc', 'fucc', 'fuckin', 'fucking', 'fck',
    'shit', 'sh1t', 'shitt', 'bullshit', 'sht',
    'bitch', 'biatch', 'biches', 'bitches', 'btch', 'b1tch',
    'ass', 'asses', 'asshole', 'ashole',
    'damn', 'dammit', 'crap', 'bastard',
    'piss', 'pissed',
    'dick', 'd1ck', 'dik', 'dicks', 'dck',
    'cock', 'kock', 'kok', 'cck',
]

SAFE_WORDS = [
    "class", "classic", "pass", "assistant",
    "compassion", "assembly", "assassin",
]


def is_safe_word(text: str) -> bool:
    return any(sw in text for sw in SAFE_WORDS)


PROFANITY_PATTERN = re.compile(
    '(' + '|'.join(re.escape(word) for word in PROFANITY_LIST) + ')',
    re.IGNORECASE
)


def contains_profanity(text: str) -> bool:
    if not text:
        return False

    cleaned = normalize(text)

    if is_safe_word(cleaned):
        return False

    return bool(PROFANITY_PATTERN.search(cleaned))


def validate_brand_name(brand_name: str):
    if not brand_name or not brand_name.strip():
        return False, "Brand name is required"
    
    clean = brand_name.strip()

    if len(clean) < 2:
        return False, "Brand name must be at least 2 characters"

    if len(clean) > 100:
        return False, "Brand name must be less than 100 characters"

    if contains_profanity(clean):
        return False, "Brand name contains inappropriate language"

    return True, None

