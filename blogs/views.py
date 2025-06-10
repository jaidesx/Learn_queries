from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import  Response
from  rest_framework.views import APIView
from  blogs.models import Blog
from blogs.serializer import BlogSerializer

# Create your views here.
class BlogList(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= 400)



class BlogDetail(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request,pk):
        try:
            blog = Blog.objects.get(id=pk)
            serializer = BlogSerializer(blog)
            return Response(serializer.data)
        except Blog.DoesNotExist:
            return Response(data={"Error":"Blog not found"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        try:
            blog = Blog.objects.get(id=pk)
            data = request.data

            serializer = BlogSerializer(blog, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
            return Response(data={"Error":"Blog not found"},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        try:
            blog = Blog.objects.get(id=pk)
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Blog.DoesNotExist:
            return Response(data={"Error":"Blog npersonal_tokenot found"},status=status.HTTP_404_NOT_FOUND)


