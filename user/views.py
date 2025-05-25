from .services.index import index as userList
from .services.create_user import create_user
from .services.dataSeedService import seedUserData

# Create your views here.
def index(request):
    return userList(request)


def create_user(request):
    return create_user(request)

def import_user(request):
    return seedUserData()