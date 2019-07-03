from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework import filters
from rest_framework.views import APIView

from murr.permissions import IsOwner
from .serializers import MurrDetailSerializer, MurrListSerializer, CommentSerializer
from .forms import CommentForm, MurrForm
from .likes import LikeProcessor
from .actions import ActionProcessor
from .models import Murr, Comment, MurrAction
from murr.shortcuts import MurrenganPaginator
from rest_framework.response import Response

User = get_user_model()


class MurrViewSet(viewsets.ModelViewSet):
    queryset = Murr.objects.all().annotate(comments_total=Count('comments__pk'), likes_total=Count('liked__pk'))
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'tags__name', 'description', 'content', 'author__username', 'categories', )
    ordering_fields = ('timestamp', 'comments_total', 'likes_total', )

    def get_serializer_class(self):
        if self.action == 'list':
            return MurrListSerializer
        return MurrDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(queryset)
        serializer = MurrListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        murr = get_object_or_404(self.queryset, pk=pk)
        serializer = MurrDetailSerializer(murr)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('timestamp', )

    def get_serializer_class(self):
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        murr_pk = self.request.query_params.get('murr', None)
        queryset = self.queryset.filter(murr_id=murr_pk)
        page = self.paginate_queryset(queryset)
        serializer = CommentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(self.queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)