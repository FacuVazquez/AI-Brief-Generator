import time
import logging
from openai import OpenAI
from django.conf import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a campaign brief generator for influencer marketing platform Collabstr.
Generate concise, professional campaign briefs based on brand requirements.
Always return exactly 3 content angles and 3 creator criteria.
Keep briefs between 4-6 sentences. Be specific and actionable."""


def build_user_prompt(brand_name, platform, goal, tone):
    return f"""Create a campaign brief for {brand_name}.
Platform: {platform}
Goal: {goal}
Tone: {tone}

Provide:
1. A brief (4-6 sentences) describing the campaign
2. Three specific content angles
3. Three creator selection criteria"""


BRIEF_SCHEMA = {
    "type": "function",
    "function": {
        "name": "generate_campaign_brief",
        "description": "Generate a structured campaign brief with angles and criteria",
        "parameters": {
            "type": "object",
            "properties": {
                "brief": {
                    "type": "string",
                    "description": "4-6 sentence campaign brief"
                },
                "angles": {
                    "type": "array",
                    "description": "Three content angle suggestions",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                },
                "criteria": {
                    "type": "array",
                    "description": "Three creator selection criteria",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                }
            },
            "required": ["brief", "angles", "criteria"]
        }
    }
}


def generate_brief_with_llm(brand_name, platform, goal, tone):
    api_key = settings.OPENAI_API_KEY
    
    if not api_key:
        logger.warning("OpenAI API key not configured - using stub response")
        return _generate_stub_response(brand_name, platform, goal, tone)
    
    try:
        client = OpenAI(api_key=api_key)
        user_prompt = build_user_prompt(brand_name, platform, goal, tone)
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            tools=[BRIEF_SCHEMA],
            tool_choice={"type": "function", "function": {"name": "generate_campaign_brief"}},
            temperature=0.3,
            max_tokens=800,
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        message = response.choices[0].message
        
        if not message.tool_calls:
            logger.error("No tool calls in response")
            return False, "No tool calls returned by API", {}
        
        tool_call = message.tool_calls[0]
        import json
        
        try:
            result = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as je:
            logger.error(f"JSON decode error: {je}")
            logger.error(f"Raw arguments: {tool_call.function.arguments[:200]}")
            return False, f"Invalid JSON response from API", {}
        
        if not all(k in result for k in ['brief', 'angles', 'criteria']):
            logger.error(f"Missing required fields in result: {result.keys()}")
            return False, "Incomplete response from API", {}
        
        metrics = {
            "latency_ms": latency_ms,
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
        }
        
        return True, result, metrics
        
    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}")
        logger.exception("Full traceback:")
        return False, str(e), {}


def _generate_stub_response(brand_name, platform, goal, tone):
    import time
    time.sleep(0.5)
    
    brief_templates = {
        'Professional': f"{brand_name} seeks to establish thought leadership on {platform}.",
        'Friendly': f"{brand_name} wants to connect authentically with audiences on {platform}.",
        'Playful': f"{brand_name} is ready to make a splash on {platform} with fun content!",
    }
    
    stub_data = {
        "brief": f"{brief_templates.get(tone, brief_templates['Professional'])} "
                 f"This {goal.lower()}-focused campaign will leverage creator partnerships to deliver "
                 f"compelling content that resonates with target audiences. "
                 f"The brand aims to maintain a {tone.lower()} voice throughout. "
                 f"Success metrics will track engagement and alignment with brand values.",
        "angles": [
            f"Behind-the-scenes look at {brand_name}'s mission and values",
            f"User testimonials and authentic {platform} stories",
            f"Educational content highlighting product benefits"
        ],
        "criteria": [
            f"Active {platform} presence with engaged audience",
            f"Content style aligns with {tone.lower()} brand tone",
            f"Track record of {goal.lower()}-driven campaigns"
        ]
    }
    
    stub_metrics = {
        "latency_ms": 500,
        "tokens_in": 0,
        "tokens_out": 0,
    }
    
    logger.info("Using stub LLM response (no API key configured)")
    return True, stub_data, stub_metrics

