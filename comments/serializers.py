from comments.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'text',
            'created_time',
            'post',
        ]
        read_only_fields = [
            'created_time',
        ]
        extra_kwargs = {
            'post': {'write_only': True}
        }
