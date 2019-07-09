from rest_framework import serializers
from posts.models import *


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_pic', 'password')
        extra_kwargs = {'email': {'write_only': True},
                        'password': {'write_only': True}
                        }

    def create(self, validated_data):
        print(validated_data)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            profile_pic=validated_data['profile_pic']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    post_created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ('id', 'user', 'post_description', 'post_created_date')


class ReactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = PostReaction
        fields = ('user', 'reaction', 'post')


class PostCommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'message', 'comment_create_date', 'post', 'commented_on_id')
        extra_kwargs = {'post': {'write_only': True}, 'commented_on_id': {'write_only': True}}


class CommentReactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment = PostCommentSerializer(read_only=True)

    class Meta:
        model = CommentReaction
        fields = ('user', 'reaction', 'comment')


class PostReactionSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    type = serializers.ListField()


class PositivePostSerializer(serializers.Serializer):
    post = serializers.IntegerField()


class ReactionMetricSerializer(serializers.Serializer):
    reaction = serializers.CharField()
    react_count = serializers.IntegerField()


class CommentReplySerializer(serializers.Serializer):
    comment = PostCommentSerializer(read_only=True)
    replies = serializers.ListField()


class CommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    commenter = serializers.DictField()
    commented_at = serializers.DateTimeField()
    comment_content = serializers.CharField()
    replies_count = serializers.IntegerField()
    reactions = PostReactionSerializer()
    replies = serializers.ListField()
    user = UserSerializer(read_only=True)


class GetPostSerializer(serializers.ModelSerializer):

    reactions = PostReactionSerializer()
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True)
    comments_count = serializers.IntegerField()
    post_created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ('id', 'user', 'post_description', 'post_created_date', 'reactions', 'comments', 'comments_count')


