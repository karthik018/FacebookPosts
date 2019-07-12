import pytest


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    from .models import User
    with django_db_blocker.unblock():
        user = User(username='karthik', profile_pic='http://karthik.png')
        user.save()
        return user.id
