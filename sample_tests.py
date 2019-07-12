import pytest
from posts.models import User, Post
from datetime import datetime
import pytz


@pytest.mark.django_db
class TestDataBase:

    def test_my_user(self):
        me = User.objects.get(username='karthik')
        assert me.is_superuser

    def test_two(self):
        User.objects.create(username='Manoj')
        count = User.objects.all().count()
        assert count == 2

    def test_three(self):
        Post.objects.create(user_id=2, post_description='Hi', post_created_date=datetime(2019, 5, 21, 20, 22, 46, tzinfo=pytz.UTC))
        count = Post.objects.count()
        assert count == 1
