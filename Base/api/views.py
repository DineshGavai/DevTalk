from rest_framework.decorators import api_view
from rest_framework.response import Response 
from Base.models import Room
from .serializers import RoomSerializers


@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    serilizer=RoomSerializers(rooms,many=True)
    return Response(serilizer.data)