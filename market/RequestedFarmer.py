from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status,permissions
from rest_framework.decorators import permission_classes
from .models import RequestTobeOwer

from .serializers import RequestTobeOwerSerializer





class RequestTobeOwnerView(APIView):
    def post(self, request):
        serilizer=RequestTobeOwerSerializer(data=request.data, context ={"request":request})
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)