from django.db import models
from posts.reactions import Reaction


class User(models.Model):
    user_name = models.CharField(max_length=15)
    profile_pic = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.user_name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_description = models.CharField(max_length=300)
    post_created_date = models.DateTimeField()

    def __str__(self):
        return self.post_description


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=5, choices=Reaction.getreactions())

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return self.reaction


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_on_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    comment_create_date = models.DateTimeField()
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.message


class CommentReaction(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=5, choices=Reaction.getreactions())

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return self.reaction

