from user.models import user_feature as UserFeature
from openai import OpenAI
from django.http import HttpResponse
from django.conf import settings
client = OpenAI(api_key = settings.OPENAI_API_KEY)


def embedding_extract(new_user, model="text-embedding-3-small", context="dating"):
    base = new_user.userbase
    
    text = ' '.join([
        str(new_user.age),
        new_user.gender or "",
        str(new_user.height),
        new_user.interests or "",
        new_user.looking_for or "",
        str(new_user.children),
        new_user.education_level or "",
        new_user.occupation or "",
        str(new_user.swiping_history),
        new_user.frequency_of_use or ""
    ])
    
    client_response = client.embeddings.create(input=[text], model=model).data[0].embedding
    featured_user = UserFeature.objects.create(feature_vector = client_response, userbase = base, context = context)
    base.preprocessed = 1
    base.save()
    return HttpResponse('User processed', featured_user)