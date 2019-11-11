from typing import Any, Dict

from rest_framework import serializers, fields

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'url',
            'title',
            'created',
        )
        model = Post
