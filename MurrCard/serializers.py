from .models import Murr, Comment
from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)



class MurrListSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SerializerMethodField()

    def get_author(self, instance):
        return instance.author.username

    class Meta:
        model = Murr
        fields = ('id', 'title', 'description', 'tags', 'comment_count', 'likes_count',
                  'timestamp', 'author', 'categories', 'featured', 'cover', 'slug')
        read_only_fields = ('id', 'title', 'description', 'tags', 'comment_count', 'likes_count',
                            'timestamp', 'author', 'categories', 'featured', 'cover', 'slug')


class MurrDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Murr
        fields = ('id', 'title', 'description', 'content', 'tags', 'comment_count', 'likes_count',
                  'timestamp', 'author', 'categories', 'featured', 'cover', 'slug')
        read_only_fields = ('id', 'timestamp', 'featured', 'slug', 'author', 'comment_count', 'likes_count',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('author', 'timestamp', 'content', 'murr', 'reply', )
