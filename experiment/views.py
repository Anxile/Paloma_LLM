from django.http import JsonResponse
from .services.similarityService import cosine_similarity

def similarity(request):
    text1 = request.GET.get("text1", "")
    text2 = request.GET.get("text2", "")
    
    result, status_code = cosine_similarity(text1, text2)
    
    return JsonResponse(result, status=status_code)