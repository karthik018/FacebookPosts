from posts.serializers import *
from posts.models import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, permissions
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F, Count


class CreatePost(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class PostList(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyToComment(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = Comment.objects.get(id=request.data['commented_on_id'])
            comment_on_id = comment.commented_on_id
            if comment_on_id is not None:
                print(comment.commented_on_id.id)
                request.data['commented_on_id'] = comment.commented_on_id.id
            post = Post.objects.get(pk=comment.post_id)
            serializer = PostCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostReact(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid():
            try:
                react = PostReaction.objects.get(user=request.user, post_id=pk)
                if react.reaction == request.data['reaction']:
                    react.delete()
                else:
                    serializer.update(instance=react, validated_data=serializer.validated_data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                serializer.save(user=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentReact(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = PostCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentReactSerializer(data=request.data)
        if serializer.is_valid():
            try:
                react = CommentReaction.objects.get(user=request.user, comment_id=pk)
                if react.reaction == request.data['reaction']:
                    react.delete()
                else:
                    serializer.update(instance=react, validated_data=serializer.validated_data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                serializer.save(user=request.user, comment=comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserPost(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPositivePosts(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        positive_posts = PostReaction.objects.values('post').annotate(
            positive_count=Count('reaction', filter=Q(reaction__in=("LIKE", "LOVE", "WOW", "HAHA"))),
            negative_count=Count('reaction', filter=Q(reaction__in=("SAD", "ANGRY")))).filter(
            positive_count__gt=F('negative_count')).values('post')
        serializer = PositivePostSerializer(positive_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPostsReactedByUser(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = PostReaction.objects.filter(user=request.user).values('post_id')
        post = Post.objects.filter(id__in=posts)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetReactionToPost(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        type = PostReaction.objects.filter(post_id=pk).values('reaction')
        count = len(type)
        reactions = {"count": count, "type": type}
        serializer = PostReactionSerializer(reactions)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetReactionMetrics(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        likes = PostReaction.objects.filter(post_id=pk).values('reaction').annotate(react_count=Count('reaction'))
        if likes.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ReactionMetricSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTotalReactionCount(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        type = PostReaction.objects.values_list('reaction', flat=True)
        count = type.count()
        serializer = PostReactionSerializer({"count": count, "type": type})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetRepliesToComment(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = IdSerializer(data=request.data)
        if serializer.is_valid():
            comment = Comment.objects.get(id=request.data['id'])
            if comment.commented_on_id is not None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            replies = Comment.objects.filter(commented_on_id=request.data['id'])
            serializer = PostCommentSerializer(replies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePost(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = IdSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.get(pk=request.data['id'])
            if post.user == request.user:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetPost(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @staticmethod
    def get_comment_data(comment):
        data = {
            "comment_id": comment['id'],
            "commenter": {
                "user_id": comment['user_id'],
                "name": comment['user__username'],
                "profile_pic": comment['user__profile_pic']
            },
            "commented_at": comment['comment_create_date'].strftime("%Y-%m-%d %H:%M:%S"),
            "comment_content": comment['message']
        }
        return data

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except:
            raise Http404
        post_reactions = PostReaction.objects.filter(post_id=pk).values_list('reaction', flat=True)
        post.reactions = {"count": post_reactions.count(), "type": list(post_reactions.distinct())}
        post_comments = Comment.objects.select_related('user').filter(post_id=pk, commented_on_id=None).values(
            'id',
            'user_id',
            'user__username',
            'user__profile_pic',
            'commented_on_id',
            'comment_create_date',
            'message')
        comments_ids = [comment['id'] for comment in post_comments]

        replies = Comment.objects.select_related('user').filter(commented_on_id__in=comments_ids).values('id',
                                                                                                         'user_id',
                                                                                                         'user__username',
                                                                                                         'user__profile_pic',
                                                                                                         'commented_on_id',
                                                                                                         'comment_create_date',
                                                                                                         'message')
        comments_ids[len(comments_ids) + 1:] = [reply['id'] for reply in replies]

        comment_reactions = CommentReaction.objects.select_related('user').filter(comment_id__in=comments_ids).values('comment_id', 'reaction')

        comment_reaction = {}
        for react in comment_reactions:
            l = []
            r = react['reaction']
            l.append(r)
            try:
                comment_reaction[react['comment_id']].append(r)

            except:
                comment_reaction[react['comment_id']] = l

        for id in comment_reaction:
            count = len(comment_reaction[id])
            reactions = list(set(comment_reaction[id]))
            data = {"count": count, "type": reactions}
            comment_reaction[id] = data

        comment_replies = {}
        for reply in replies:
            comment_reply = []
            d = self.get_comment_data(reply)
            try:
                d["reactions"] = comment_reaction[reply['id']]
            except:
                d["reactions"] = {"count": 0, "type": []}
            comment_reply.append(d)
            try:
                comment_replies[reply['commented_on_id']].append(d)
            except:
                comment_replies[reply['commented_on_id']] = comment_reply
        comments = []
        for comment in post_comments:
            d = self.get_comment_data(comment)
            try:
                d["reactions"] = comment_reaction[comment['id']]
                d["replies_count"] = len(comment_replies[comment['id']])
                d["replies"] = comment_replies[comment['id']]
            except KeyError:
                d["reactions"] = {"count": 0, "type": []}
                d["replies_count"] = 0
                d["replies"] = []
            comments.append(d)
        post.comments = comments
        post.comments_count = len(comments)
        serializer = GetPostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
