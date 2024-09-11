# blog_api/views.py

from rest_framework import generics
from .models import BlogPost
from .serializers import BlogEntrySerializer,RegisterSerializer
from .tasks import index_blog_post
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully.",
        }, status=status.HTTP_201_CREATED)

class BlogEntryView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        blog_post = serializer.save()
        index_blog_post.delay(blog_post.id)

class SearchView(generics.ListAPIView):
    serializer_class = BlogEntrySerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if not query:
            return BlogPost.objects.none()

        s = Search(index='elastic_demo')
        q = MultiMatch(query=query, fields=['title', 'text'])
        s = s.query(q)
        response = s.execute()

        blog_ids = [hit.meta.id for hit in response]
        return BlogPost.objects.filter(id__in=blog_ids)