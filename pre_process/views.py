from django.http import HttpResponse
from .services.embeddingService import embedding_extract

# Create your views here.
def process_data(request):
    return embedding_extract(request)