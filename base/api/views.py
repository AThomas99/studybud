from rest_framework.decorators import api_view
from rest_framework.response import Response


from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

# Returns an API of all rooms
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serialzer = RoomSerializer(rooms, many=True)
    return Response(serialzer.data)


# Returns an API of a single room
@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serialzer = RoomSerializer(room, many=False)
    return Response(serialzer.data)