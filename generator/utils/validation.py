from .profanity import validate_brand_name

VALID_PLATFORMS = ['Instagram', 'TikTok', 'UGC']
VALID_GOALS = ['Awareness', 'Conversions', 'Content Assets']
VALID_TONES = ['Professional', 'Friendly', 'Playful']


def validate_input(data):
    errors = []
    
    brand_name = data.get('brand_name', '').strip()
    is_valid, error = validate_brand_name(brand_name)
    if not is_valid:
        errors.append(error)
    
    platform = data.get('platform', '')
    if platform not in VALID_PLATFORMS:
        errors.append(f"Platform must be one of: {', '.join(VALID_PLATFORMS)}")
    
    goal = data.get('goal', '')
    if goal not in VALID_GOALS:
        errors.append(f"Goal must be one of: {', '.join(VALID_GOALS)}")
    
    tone = data.get('tone', '')
    if tone not in VALID_TONES:
        errors.append(f"Tone must be one of: {', '.join(VALID_TONES)}")
    
    if errors:
        return False, '; '.join(errors), None
    
    cleaned_data = {
        'brand_name': brand_name,
        'platform': platform,
        'goal': goal,
        'tone': tone,
    }
    
    return True, None, cleaned_data

