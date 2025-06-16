from django.http import HttpResponse
from .services.embeddingService import embedding_extract
from user.models.user import User

# Create your views here.
def process_data(request):
    users = User.objects.all()
    for user in users:
        if not user.userbase.preprocessed:
            embedding_extract(user)
            print("{user.username} processed")
        else:
            print(f"{user.userbase.name} already processed")
    return HttpResponse('Data processed for all users')

        
    