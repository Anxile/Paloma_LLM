from user.models.user_feature import UserFeature
from openai import OpenAI
from django.http import HttpResponse
from django.conf import settings
client = OpenAI(api_key = settings.OPENAI_API_KEY)


def embedding_extract(user, model="text-embedding-3-small", context="dating"):
    base = user.userbase
    
    text = ' '.join([
        str(user.age),
        user.gender or "",
        str(user.height),
        user.interests or "",
        user.looking_for or "",
        str(user.children),
        user.education_level or "",
        user.occupation or "",
        str(user.swiping_history),
        user.frequency_of_use or ""
    ])
    
    client_response = client.embeddings.create(input=[text], model=model).data[0].embedding
    featured_user = UserFeature.objects.create(feature_vector = client_response, userbase = base, context = context)
    base.preprocessed = 1
    base.save()
    return HttpResponse('User processed', featured_user)