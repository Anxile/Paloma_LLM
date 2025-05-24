from .services.index import index
from .services.create_user import create_user
from .services.dataSeedService import import_user

# Create your views here.
def index(request):
    return index(request)


def create_user(request):
    return create_user(request)

def import_user(request):
    return import_user(request)