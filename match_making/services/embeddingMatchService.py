from api.views import compute_similarity
from user.models import UserBase, User, UserFeature
from pre_process.services.embeddingService import embedding_extract
from .rankingService import ranking
from django.http import JsonResponse


def user_match(request, userid):
    candidates = []
    user = UserBase.objects.get(id=userid)
    collection = UserBase.objects.all()
    if user.preprocessed:
        for match in collection:
            if match.id == user.id:
                continue
            if not match.preprocessed:
                embedding_extract(User.objects.get(userbase=match))
            sim = compute_similarity(user, match)
            candidates.append((match, sim))
    else:
        embedding_extract(User.objects.get(userbase=user))
    top_candidates = ranking(candidates)
    return JsonResponse(request, {'user': user, 'candidates': top_candidates})