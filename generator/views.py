import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .utils.validation import validate_input
from .services.llm import generate_brief_with_llm

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def generate_brief(request):
    try:
        data = json.loads(request.body)
        
        is_valid, error_message, cleaned_data = validate_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {error_message}")
            return JsonResponse({
                'success': False,
                'error': error_message
            }, status=400)
        
        success, result, metrics = generate_brief_with_llm(
            brand_name=cleaned_data['brand_name'],
            platform=cleaned_data['platform'],
            goal=cleaned_data['goal'],
            tone=cleaned_data['tone']
        )
        
        if not success:
            logger.error(f"LLM generation failed: {result}")
            return JsonResponse({
                'success': False,
                'error': f'Failed to generate brief: {result}'
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'data': {
                'brief': result['brief'],
                'angles': result['angles'],
                'criteria': result['criteria'],
            },
            'metrics': {
                'latency_ms': metrics.get('latency_ms', 0),
                'tokens_in': metrics.get('tokens_in', 0),
                'tokens_out': metrics.get('tokens_out', 0),
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        logger.exception("Unexpected error in generate_brief")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred'
        }, status=500)
