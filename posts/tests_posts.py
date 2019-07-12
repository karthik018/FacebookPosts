from .operations import *
import pytest
from .models import User
import unittest
from django.db import IntegrityError
from datetime import datetime
import pytz


@pytest.mark.django_db
class TestPosts:

    def test_post_creation(self, django_db_setup):
        count_before = Post.objects.count()
        user_id = django_db_setup
        post_id = create_post(user_id=user_id, post_content="Hello")
        count = Post.objects.count()
        assert count == count_before + 1

    def test_post_content(self, django_db_setup):
        user_id = django_db_setup
        post_id = create_post(user_id=user_id, post_content="Hello")
        post = Post.objects.get(id=post_id)
        assert post.post_description == "Hello"

    def test_post_user(self, django_db_setup):
        user_id = django_db_setup
        post_id = create_post(user_id=user_id, post_content="Hello")
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=user_id)
        assert post.user == user


@pytest.mark.django_db
class TestComment:

    @pytest.fixture
    def setup_data(cls, django_db_setup):
        user_id = django_db_setup
        Post.objects.create(user_id=user_id, post_description="Hello",
                            post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        post = Post.objects.latest('id')
        return post.id, user_id

    def test_comment_creation(self, setup_data):
        post_id, user_id = setup_data
        count_before = Comment.objects.filter(post_id=post_id, commented_on_id=None).count()
        comment_id = add_comment(post_id=post_id, comment_user_id=user_id, comment_text="Hii")
        assert Comment.objects.count() == count_before + 1

    def test_comment_content(self, setup_data):
        post_id, user_id = setup_data
        comment_id = add_comment(post_id=post_id, comment_user_id=user_id, comment_text="Hii")
        assert Comment.objects.get(id=comment_id).message == "Hii"

    def test_comment_user(self, setup_data):
        post_id, user_id = setup_data
        comment_id = add_comment(post_id=post_id, comment_user_id=user_id, comment_text="Hii")
        assert Comment.objects.get(id=comment_id).user.username == 'karthik'

    def test_comment_post(self, setup_data):
        post_id, user_id = setup_data
        comment_id = add_comment(post_id=post_id, comment_user_id=user_id, comment_text="Hii")
        assert Comment.objects.get(id=comment_id).post == Post.objects.get(id=1)


@pytest.mark.django_db
class TestCommentReply:

    @pytest.fixture
    def setup_data(cls, django_db_setup):
        user_id = django_db_setup
        post = Post.objects.create(user_id=user_id, post_description="Hello",
                                   post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        comment = Comment.objects.create(post_id=post.id, user_id=user_id, commented_on_id=None,
                                         comment_create_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC),
                                         message="Hii")
        return post.id, comment.id, user_id

    def test_reply_creation(self, setup_data):
        post_id, comment_id, user_id = setup_data
        count_before = Comment.objects.filter(commented_on_id=comment_id).count()
        reply_to_comment(comment_id=comment_id, reply_user_id=user_id, reply_text="Haii")
        replies = Comment.objects.filter(commented_on_id=comment_id).count()
        assert replies == count_before + 1

    def test_reply_comment(self, setup_data):
        post_id, comment_id, user_id = setup_data
        reply_id = reply_to_comment(comment_id=comment_id, reply_user_id=user_id, reply_text="Haii")
        reply = Comment.objects.get(id=reply_id)
        assert reply.commented_on_id.id == comment_id

    def test_reply_reply(self, setup_data):
        post_id, comment_id, user_id = setup_data
        first_reply_id = reply_to_comment(comment_id=comment_id, reply_user_id=user_id, reply_text="Haii")
        second_reply_id = reply_to_comment(comment_id=first_reply_id, reply_user_id=user_id, reply_text="Haii")
        reply = Comment.objects.get(id=second_reply_id)
        assert reply.commented_on_id.id == comment_id


@pytest.mark.django_db
class TestPostReaction:

    @pytest.fixture
    def setup_data(self, django_db_setup):
        user_id = django_db_setup
        post = Post.objects.create(user_id=user_id, post_description="Hello", post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        return post.id, user_id

    def test_react_creation(self, setup_data):
        post_id, user_id = setup_data
        count_before = PostReaction.objects.filter(post_id=post_id).count()
        react_to_post(user_id=user_id, post_id=post_id, reaction_type="LOVE")
        count = PostReaction.objects.filter(post_id=post_id).count()
        reaction = PostReaction.objects.latest('id')
        assert count == count_before + 1
        assert reaction.reaction == "LOVE"
        assert reaction.user_id == user_id

    def test_user_reaction_to_post(self, setup_data):
        post_id, user_id = setup_data
        reaction = react_to_post(user_id=user_id, post_id=post_id, reaction_type="LIKE")
        reaction = react_to_post(user_id=user_id, post_id=post_id, reaction_type="LIKE")
        with pytest.raises(PostReaction.DoesNotExist):
            PostReaction.objects.get(post_id=post_id, user_id=user_id)

    def test_user_reaction_change(self, setup_data):
        post_id, user_id = setup_data
        first_reaction = react_to_post(user_id=user_id, post_id=post_id, reaction_type="WOW")
        second_reaction = react_to_post(user_id=user_id, post_id=post_id, reaction_type="LOVE")
        reaction = PostReaction.objects.latest('id')
        assert first_reaction == second_reaction
        assert reaction.id == first_reaction
        assert reaction.reaction == "LOVE"


@pytest.mark.django_db
class TestCommentReaction:

    @pytest.fixture
    def setup_data(self, django_db_setup):
        user_id = django_db_setup
        post = Post.objects.create(user_id=user_id, post_description="Hello",
                                   post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        comment = Comment.objects.create(post_id=post.id, user_id=user_id, commented_on_id=None,
                                         comment_create_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC),
                                         message="Hii")
        return post.id, comment.id, user_id

    def test_react_creation(self, setup_data):
        post_id, user_id, comment_id = setup_data
        count_before = CommentReaction.objects.filter(comment_id=comment_id).count()
        react_to_comment(user_id=user_id, comment_id=comment_id, reaction_type="LIKE")
        count = CommentReaction.objects.filter(comment_id=comment_id).count()
        reaction = CommentReaction.objects.latest('id')
        assert count == count_before + 1
        assert reaction.reaction == "LIKE"
        assert reaction.user_id == user_id

    def test_user_reaction_to_comment(self, setup_data):
        post_id, user_id, comment_id = setup_data
        reaction = react_to_comment(user_id=user_id, comment_id=comment_id, reaction_type="LOVE")
        reaction = react_to_comment(user_id=user_id, comment_id=comment_id, reaction_type="LOVE")
        with pytest.raises(CommentReaction.DoesNotExist):
            CommentReaction.objects.get(comment_id=comment_id, user_id=user_id)

    def test_user_reaction_changed(self, setup_data):
        post_id, user_id, comment_id = setup_data
        first_reaction = react_to_comment(user_id=user_id, comment_id=comment_id, reaction_type="LOVE")
        second_reaction = react_to_comment(user_id=user_id, comment_id=comment_id, reaction_type="WOW")
        reaction = CommentReaction.objects.latest('id')
        assert first_reaction == second_reaction
        assert reaction.id == first_reaction
        assert reaction.reaction == "WOW"


@pytest.mark.django_db
class TestUserPosts:

    @pytest.fixture
    def setup_data(self, django_db_setup):
        user_id = django_db_setup
        first_post = Post.objects.create(user_id=user_id, post_description="first post", post_created_date=datetime.now(pytz.utc))
        second_post = Post.objects.create(user_id=user_id, post_description="second post", post_created_date=datetime.now(pytz.utc))
        third_post = Post.objects.create(user_id=user_id, post_description="third post", post_created_date=datetime.now(pytz.utc))
        fourth_post = Post.objects.create(user_id=user_id, post_description="fourth post", post_created_date=datetime.now(pytz.utc))
        return user_id, first_post.id, second_post.id, third_post.id, fourth_post.id

    def test_user_posts(self, setup_data):
        user_id, first_post_id, second_post_id, third_post_id, fourth_post_id = setup_data
        user_posts = get_user_posts(user_id=user_id)
        assert len(user_posts) == 4

    def test_user_posts_data(self, setup_data):
        user_id, first_post_id, second_post_id, third_post_id, fourth_post_id = setup_data
        user_posts = [post["post_id"] for post in get_user_posts(user_id=user_id)]
        assert first_post_id in user_posts
        assert second_post_id in user_posts
        assert third_post_id in user_posts
        assert fourth_post_id in user_posts

    def test_user_posts_two(self, setup_data):
        user_id = setup_data
        second_user = User.objects.create(username='Bharat', profile_pic="http://bharat.png")
        post = Post.objects.create(user_id=second_user.id, post_description="first post of second user", post_created_date=datetime.now(pytz.utc))
        first_user_posts = [post["post_id"] for post in get_user_posts(user_id=user_id)]
        assert post.id not in first_user_posts


@pytest.mark.django_db
class TestPostsWithMorePositiveReactions:

    @pytest.fixture
    def setup_post_data(self, django_db_setup):
        user_id = django_db_setup
        second_user = User.objects.create(username='Manoj', profile_pic="http://manoj.png")
        third_user = User.objects.create(username='Bharat')
        fourth_user = User.objects.create(username='Krishna')
        first_post = Post.objects.create(user_id=user_id, post_description="first post", post_created_date=datetime.now(pytz.utc))
        second_post = Post.objects.create(user_id=user_id, post_description="second post", post_created_date=datetime.now(pytz.utc))
        return user_id, second_user.id, third_user.id, fourth_user.id, first_post.id, second_post.id

    @pytest.fixture
    def setup_post_reaction_data(self, setup_post_data):
        user_id, second_user_id, third_user_id, fourth_user_id, first_post_id, second_post_id = setup_post_data
        PostReaction.objects.create(user_id=user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=second_user_id, post_id=first_post_id, reaction="LOVE")
        PostReaction.objects.create(user_id=third_user_id, post_id=first_post_id, reaction="HAHA")
        PostReaction.objects.create(user_id=fourth_user_id, post_id=first_post_id, reaction="SAD")
        PostReaction.objects.create(user_id=user_id, post_id=second_post_id, reaction="WOW")
        PostReaction.objects.create(user_id=second_user_id, post_id=second_post_id, reaction="SAD")
        PostReaction.objects.create(user_id=third_user_id, post_id=second_post_id, reaction="ANGRY")
        PostReaction.objects.create(user_id=fourth_user_id, post_id=second_post_id, reaction="SAD")

    def test_posts_with_more_postive_reactions(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, third_user_id, fourth_user_id, first_post_id, second_post_id = setup_post_data
        positive_posts = get_posts_with_more_positive_reactions()
        assert first_post_id in positive_posts

    def test_positive_posts_negative_reactions(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, third_user_id, fourth_user_id, first_post_id, second_post_id = setup_post_data
        positive_posts = get_posts_with_more_positive_reactions()
        assert second_post_id not in positive_posts


@pytest.mark.django_db
class TestPostsReactedByUser:

    @pytest.fixture
    def setup_post_data(self, django_db_setup):
        user_id = django_db_setup
        second_user = User.objects.create(username='Manoj', profile_pic="http://manoj.png")
        third_user = User.objects.create(username='Bharat')
        first_post = Post.objects.create(user_id=user_id, post_description="first post", post_created_date=datetime.now(pytz.utc))
        second_post = Post.objects.create(user_id=user_id, post_description="second post", post_created_date=datetime.now(pytz.utc))
        third_post = Post.objects.create(user_id=user_id, post_description="third post", post_created_date=datetime.now(pytz.utc))
        return user_id, second_user.id, third_user.id, first_post.id, second_post.id, third_post.id

    @pytest.fixture
    def setup_post_reaction_data(self, setup_post_data):
        user_id, second_user_id, third_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        PostReaction.objects.create(user_id=user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=second_user_id, post_id=first_post_id, reaction="LOVE")
        PostReaction.objects.create(user_id=third_user_id, post_id=third_post_id, reaction="HAHA")
        PostReaction.objects.create(user_id=user_id, post_id=second_post_id, reaction="WOW")
        PostReaction.objects.create(user_id=second_user_id, post_id=second_post_id, reaction="SAD")
        PostReaction.objects.create(user_id=third_user_id, post_id=second_post_id, reaction="ANGRY")

    def test_posts_reacted_by_first_user(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, third_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        posts = [post["post_id"] for post in get_posts_reacted_by_user(user_id=user_id)]
        assert first_post_id in posts
        assert second_post_id in posts

    def test_posts_reacted_by_second_user(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, third_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        posts = [post["post_id"] for post in get_posts_reacted_by_user(user_id=second_user_id)]
        assert first_post_id in posts
        assert second_post_id in posts


@pytest.mark.django_db
class TestPostReactions:

    @pytest.fixture
    def setup_post_data(self, django_db_setup):
        user_id = django_db_setup
        second_user = User.objects.create(username='Manoj', profile_pic="http://manoj.png")
        third_user = User.objects.create(username='Bharat')
        first_post = Post.objects.create(user_id=user_id, post_description="first post",
                                         post_created_date=datetime.now(pytz.utc))
        second_post = Post.objects.create(user_id=user_id, post_description="second post",
                                          post_created_date=datetime.now(pytz.utc))
        third_post = Post.objects.create(user_id=user_id, post_description="third post",
                                         post_created_date=datetime.now(pytz.utc))
        return user_id, second_user.id, third_user.id, first_post.id, second_post.id, third_post.id

    @pytest.fixture
    def setup_post_reaction_data(self, setup_post_data):
        user_id, second_user_id, third_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        PostReaction.objects.create(user_id=user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=second_user_id, post_id=first_post_id, reaction="LOVE")
        PostReaction.objects.create(user_id=third_user_id, post_id=third_post_id, reaction="HAHA")
        PostReaction.objects.create(user_id=user_id, post_id=second_post_id, reaction="WOW")
        PostReaction.objects.create(user_id=second_user_id, post_id=second_post_id, reaction="SAD")
        PostReaction.objects.create(user_id=third_user_id, post_id=second_post_id, reaction="ANGRY")

    def test_reactions_by_user_to_post(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, third_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        post_reactions = get_reactions_to_post(first_post_id)
        assert post_reactions[0]["user_id"] == user_id
        assert post_reactions[1]["user_id"] == second_user_id

    def test_reactions_to_post(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, third_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        post_reactions = get_reactions_to_post(second_post_id)
        assert post_reactions[0]['reaction'] == "WOW"
        assert post_reactions[1]['reaction'] == "SAD"
        assert post_reactions[2]['reaction'] == "ANGRY"


@pytest.mark.django_db
class TestReactionMetrics:

    @pytest.fixture
    def setup_post_data(self, django_db_setup):
        user_id = django_db_setup
        second_user = User.objects.create(username='Manoj', profile_pic="http://manoj.png")
        first_post = Post.objects.create(user_id=user_id, post_description="first post",
                                         post_created_date=datetime.now(pytz.utc))
        second_post = Post.objects.create(user_id=user_id, post_description="second post",
                                          post_created_date=datetime.now(pytz.utc))
        third_post = Post.objects.create(user_id=user_id, post_description="third post",
                                         post_created_date=datetime.now(pytz.utc))
        return user_id, second_user.id, first_post.id, second_post.id, third_post.id

    @pytest.fixture
    def setup_post_reaction_data(self, setup_post_data):
        user_id, second_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        PostReaction.objects.create(user_id=user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=second_user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=user_id, post_id=second_post_id, reaction="WOW")
        PostReaction.objects.create(user_id=second_user_id, post_id=second_post_id, reaction="SAD")

    def test_reaction_metrics(self, setup_post_data, setup_post_reaction_data):
        user_id, second_user_id, first_post_id, second_post_id, third_post_id = setup_post_data
        reaction_metrics = get_reaction_metrics(first_post_id)
        assert reaction_metrics["LIKE"] == 2
        reaction_metrics = get_reaction_metrics(second_post_id)
        assert reaction_metrics["WOW"] == 1
        assert reaction_metrics["SAD"] == 1
        reaction_metrics = get_reaction_metrics(third_post_id)
        with pytest.raises(KeyError):
            reaction_metrics["LIKE"]


@pytest.mark.django_db
class TestReactionCount:

    @pytest.fixture
    def setup_post_data(self, django_db_setup):
        user_id = django_db_setup
        second_user = User.objects.create(username='Manoj', profile_pic="http://manoj.png")
        first_post = Post.objects.create(user_id=user_id, post_description="first post",
                                         post_created_date=datetime.now(pytz.utc))
        second_post = Post.objects.create(user_id=user_id, post_description="second post",
                                          post_created_date=datetime.now(pytz.utc))
        return user_id, second_user.id, first_post.id, second_post.id

    @pytest.fixture
    def setup_post_reaction_data(self, setup_post_data):
        user_id, second_user_id, first_post_id, second_post_id = setup_post_data
        PostReaction.objects.create(user_id=user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=second_user_id, post_id=first_post_id, reaction="LIKE")
        PostReaction.objects.create(user_id=user_id, post_id=second_post_id, reaction="WOW")
        PostReaction.objects.create(user_id=second_user_id, post_id=second_post_id, reaction="SAD")

    def test_total_reaction_count(self, setup_post_reaction_data):
        assert get_total_reaction_count() == 4


@pytest.mark.django_db
class TestRepliesForComment:

    @pytest.fixture
    def setup_data(cls, django_db_setup):
        user_id = django_db_setup
        post = Post.objects.create(user_id=user_id, post_description="Hello",
                                   post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        comment = Comment.objects.create(post_id=post.id, user_id=user_id, commented_on_id=None,
                                         comment_create_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC),
                                         message="Hii")
        return post.id, comment.id, user_id

    @pytest.fixture
    def setup_data_for_comment_replies(self, setup_data):
        post_id, comment_id, user_id = setup_data
        first_reply_id = reply_to_comment(comment_id=comment_id, reply_user_id=user_id, reply_text="Haii")
        second_reply_id = reply_to_comment(comment_id=comment_id, reply_user_id=user_id, reply_text="Haii")
        return post_id, comment_id, user_id, first_reply_id, second_reply_id

    def test_for_asking_replies_not_to_comment(self, setup_data_for_comment_replies):
        post_id, comment_id, user_id, first_reply_id, second_reply_id = setup_data_for_comment_replies
        with pytest.raises(SuspiciousOperation):
            get_replies_for_comment(first_reply_id)

    def test_replies_to_comment(self, setup_data_for_comment_replies):
        post_id, comment_id, user_id, first_reply_id, second_reply_id = setup_data_for_comment_replies
        replies = get_replies_for_comment(comment_id=comment_id)
        assert replies[0]["comment_id"] == first_reply_id
        assert replies[1]["comment_id"] == second_reply_id

    def test_replied_user(self, setup_data_for_comment_replies):
        post_id, comment_id, user_id, first_reply_id, second_reply_id = setup_data_for_comment_replies
        replies = get_replies_for_comment(comment_id=comment_id)
        assert replies[0]["commenter"]["user_id"] == user_id


@pytest.mark.django_db
class TestDeletePost:

    @pytest.fixture
    def setup_data(cls, django_db_setup):
        user_id = django_db_setup
        post = Post.objects.create(user_id=user_id, post_description="Hello", post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        return post.id

    def test_post_deletion(self, setup_data):
        post_id = setup_data
        delete_post(post_id=post_id)
        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=post_id)

    def test_deletion_of_post_not_there(self, setup_data):
        post_id = 2
        with pytest.raises(Post.DoesNotExist):
            delete_post(post_id=post_id)


@pytest.mark.django_db
class TestGetPost:

    @pytest.fixture
    def setup_data(self, django_db_setup):
        user_id = django_db_setup
        second_user = User.objects.create(username="Manoj", profile_pic="http://manoj.png")
        post = Post.objects.create(user_id=user_id, post_description="first post", post_created_date=datetime.now(pytz.utc))
        first_comment = Comment.objects.create(post_id=post.id, user_id=user_id, comment_create_date=datetime.now(pytz.utc), message="first comment")
        second_comment = Comment.objects.create(post_id=post.id, user_id=second_user.id, comment_create_date=datetime.now(pytz.utc), message="second comment")
        first_reply = Comment.objects.create(post_id=post.id, user_id=second_user.id, commented_on_id=first_comment, comment_create_date=datetime.now(pytz.utc), message="first reply")
        second_reply = Comment.objects.create(post_id=post.id, user_id=user_id, commented_on_id=second_comment, comment_create_date=datetime.now(pytz.utc), message="second reply")
        first_reaction = PostReaction.objects.create(post_id=post.id, user_id=user_id, reaction="LOVE")
        second_reaction = PostReaction.objects.create(post_id=post.id, user_id=second_user.id, reaction="LOVE")
        first_comment_reaction = CommentReaction.objects.create(comment_id=first_comment.id, user_id=user_id, reaction="LIKE")
        second_comment_reaction = CommentReaction.objects.create(comment_id=first_reply.id, user_id=second_user.id, reaction="LIKE")

        return user_id, second_user, post, first_comment, second_comment, first_reply, second_reply, first_reaction, second_reaction, first_comment_reaction, second_comment_reaction

    def test_post_data(self, setup_data):
        user_id, second_user, post, first_comment, second_comment, first_reply, second_reply, first_reaction, second_reaction, first_comment_reaction, second_comment_reaction = setup_data
        user = User.objects.get(id=user_id)
        post_data = get_post(post.id)
        assert post_data["post_id"] == post.id
        assert post_data["posted_by"] == {"name": user.username, "user_id": user.id, "profile_pic_url": user.profile_pic}
        assert post_data["posted_at"] == post.post_created_date.strftime("%Y-%m-%d %H:%M:%S")
        assert post_data["post_content"] == post.post_description
        reaction_count = PostReaction.objects.filter(post_id=post.id).count()
        assert post_data["reactions"] == {"count": reaction_count, "type": ["LOVE"]}
        comment_count = Comment.objects.filter(post_id=post.id, commented_on_id=None).count()
        assert post_data["comments_count"] == comment_count

    def test_comment_data(self, setup_data):
        user_id, second_user, post, first_comment, second_comment, first_reply, second_reply, first_reaction, second_reaction, first_comment_reaction, second_comment_reaction = setup_data
        user = User.objects.get(id=user_id)
        post_data = get_post(post.id)
        assert post_data["comments"][0]["comment_id"] == first_comment.id
        assert post_data["comments"][0]["commenter"] == {"user_id": user.id, "name": user.username, "profile_pic_url": user.profile_pic}
        assert post_data["comments"][0]["commented_at"] == first_comment.comment_create_date.strftime("%Y-%m-%d %H:%M:%S")
        assert post_data["comments"][0]["comment_content"] == first_comment.message


if __name__ == '__main__':
    unittest.main()
