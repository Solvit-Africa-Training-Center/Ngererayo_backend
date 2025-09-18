from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import (ConsultantSerializer,
                          RequestTobeConsultantSerializer,
                          ConsultantPostSerializer)
from .models import (Consultant,ConsultantPost,
                     RequestTobeConsultant,
                     ConsultantFollow)





class ConsultantListView(APIView):
    def get(self, request):
        consutant=Consultant.objects.all()
        serializer=ConsultantSerializer(consutant,many=True)
        return Response(serializer.data)
    


class FollowConsultantview(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request,consultant_id):
        consultant=Consultant.objects.get(id=consultant_id)
        follow, created=ConsultantFollow.objects.get_or_create(user=request.user,consultant=consultant)    
        if created:
            return Response({"message":"You are now following this consultant."},status=status.HTTP_201_CREATED)
        else:
            follow.delete()
            return Response({"message":"You have unfollowed this consultant."},status=status.HTTP_200_OK)
        



class FollowConsultantPostView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        followed_consultants=ConsultantFollow.objects.filter(user=request.user).values_list('consultant_id',flat=True)
        followed_posts=ConsultantPost.objects.filter(consultant_id__in=followed_consultants)
        serializer=ConsultantPostSerializer(followed_posts,many=True)
        return Response(serializer.data)




class RequestTobeConsultantView(APIView):
    def post(self, request):
        serializer=RequestTobeConsultantSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)