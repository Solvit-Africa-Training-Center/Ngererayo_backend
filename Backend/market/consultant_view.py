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




class ConsultantAddPostView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
         try:
             consultant=request.user.consultant
         except Consultant.DoesNotExist:
                return Response({"error":"You are not a consultant"},status=status.HTTP_403_FORBIDDEN)
         serializer=ConsultantPostSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save(consultant=consultant)
             return Response(serializer.data,status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    





class ConsultantPostsView(APIView):
    def get(self,request, consultant_id):
        posts=ConsultantPost.objects.filter(consultant_id=consultant_id)
        serializer=ConsultantPostSerializer(posts,many=True)
        return Response(serializer.data)



class ConsultantEditPostView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def put(self, request,post_id):
        try:
            post=ConsultantPost.objects.get(id=post_id)
        except ConsultantPost.DoesNotExist:
            return Response({"error":"Post not found"},status=status.HTTP_404_NOT_FOUND)
        if post.consultant.user !=request.user:
            return Response({"error":"You do not have permission to edit this post"},status=status.HTTP_403_FORBIDDEN)   
        serializer=ConsultantPostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK) 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ConsultantDeletePostView(APIView):
    def Delete(self, request,post_id):
        try:
            post=ConsultantPost.objects.get(id=post_id)
        except ConsultantPost.DoesNotExist:
            return Response({"error":"Post not found"},status=status.HTTP_404_NOT_FOUND)
        if post.consultant.user !=request.user:
            return Response({"error":"You do not have permission to delete this post"},status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message":"Post deleted successfully"},status=status.HTTP_200_OK)
     