from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status,permissions
from rest_framework.decorators import permission_classes
from .models import Order

from .serializers import OrderSerialzier






class PlaceOrderView(APIView):
    permission_classes =[permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        serilaizer=OrderSerialzier(data=request.data,context={'request':request})

        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)