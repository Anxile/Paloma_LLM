from .services.embeddingMatchService import user_match

def match_making(request):
    return user_match(request, request.user.id)