from .models import User, Post, CommentReaction, Comment, PostReaction
from django.utils import timezone as t


def get_post(post_id):
    post = Post.objects.get(id=post_id)
    posted_by = {"name": post.user.user_name, "user_id": post.user_id, "profile_pic_url": post.user.profile_pic}
    posted_at = post.post_created_date
    posted_at = ' '.join([str(posted_at.date()), str(posted_at.time())])
    post_content = post.post_description
    post_likes = PostReaction.objects.filter(post_id=post_id)
    post_reactions = post_likes.values('reaction').distinct()
    comments = Comment.objects.filter(post_id=post_id, commented_on_id=None)
    comments_count = comments.count()
    post_comments = []
    for comment in comments:
        post_replies = []
        commenter = {"user_id": comment.user_id, "name": comment.user.user_name,
                     "profile_pic_url": comment.user.profile_pic}
        commented_at = comment.comment_create_date
        commented_at = ' '.join([str(commented_at.date()), str(commented_at.time())])
        reaction = CommentReaction.objects.filter(id=comment.id)
        reaction_count = reaction.count()
        reactions = reaction.values('reaction')
        comment_reactions = {"count": reaction_count, "type": reactions}
        replies = Comment.objects.filter(post_id=post_id, commented_on_id=comment.id)
        replies_count = replies.count()
        for reply in replies:
            replied_at = reply.comment_create_date
            replied_at = ' '.join([str(replied_at.date()), str(replied_at.time())])
            reply_reaction = CommentReaction.objects.filter(comment_id=reply.id)
            reply_react_count = reply_reaction.count()
            reply_react_type = reply_reaction.values('reaction')
            replier = {"comment_id": reply.comment_id,
                       "commenter": {"user_id": reply.user_id, "name": reply.user.user_name,
                                     "profile_pic_url": reply.user.profile_pic}, "commented_at": replied_at,
                       "comment_content": reply.message,
                       "reactions": {"count": reply_react_count, "type": reply_react_type}}
            post_replies.append(replier)
        post_comment = {"comment_id": comment.id, "commenter": commenter, "commented_at": commented_at,
                        "comment_content": comment.message, "reactions": comment_reactions,
                        "replies_count": replies_count, "replies": post_replies}
        post_comments.append(post_comment)

    result = {"post_id": post_id, "posted_by": posted_by, "posted_at": posted_at, "post_content": post_content,
              "reactions": post_reactions, "comments": post_comments, "comments_count": comments_count}
    return result


def create_post(user_id, post_content):
    post = Post(user_id=user_id, post_description=post_content, post_created_date=t.now())
    post.save()
    return post.id


def add_comment(post_id, comment_user_id, comment_text):
    comment = Comment(post_id=post_id, user_id=comment_user_id, comment_create_date=t.now(), message=comment_text)
    comment.save()
    return comment.id


def reply_to_comment(comment_id, reply_user_id, reply_text):
    comment = Comment.objects.get(id=comment_id)
    comment_on_id = comment.commented_on_id
    if comment_on_id is not None:
        comment = Comment.objects.get(id=comment.commented_on_id.id)
    reply = Comment(post_id=comment.post_id, user_id=reply_user_id, commented_on_id=comment,
                    comment_create_date=t.now(),
                    message=reply_text)
    reply.save()
    return reply.id


def react_to_post(user_id, post_id, reaction_type):
    try:
        react = PostReaction.objects.get(user_id=user_id, post_id=post_id)
        if react.reaction == reaction_type:
            react.delete()
        else:
            reaction_type = reaction_type
            react.reaction = reaction_type
            react.save()
    except:
        react = PostReaction(user_id=user_id, post_id=post_id, reaction=reaction_type)
        react.save()


def react_to_comment(user_id, comment_id, reaction_type):
    try:
        react = CommentReaction.objects.get(user_id=user_id, comment_id=comment_id)
        if react.reaction == reaction_type:
            react.delete()
        else:
            reaction_type = reaction_type
            react.reaction = reaction_type
            react.save()
    except:
        react = CommentReaction(user_id=user_id, comment_id=comment_id, reaction=reaction_type)
        react.save()


def get_user_posts(user_id):
    posts_list = []
    posts = Post.objects.filter(user_id=user_id)
    for post in posts:
        posts_list.append(get_post(post.id))

    return posts_list


# def get_posts_with_more_positive_reactions():
#     posts = Posts.objects.all()
#     positive_posts = []
#     for post in posts:
#         p = Posts.objects.get(post_id=post.post_id)
#         l = Likes.objects.filter(post_id=p)
#         reactions = l.values('reaction')
#         reactions = getreactiontype(reactions)
#         positive_reactions = ["LIKE", "LOVE", "WOW", "HAHA"]
#         negative_reactions = ["SAD", "ANGRY"]
#         positive = 0
#         negative = 0
#         for react in reactions:
#             if react in positive_reactions:
#                 positive += 1
#             elif react in negative_reactions:
#                 negative += 1
#         if positive > negative:
#             positive_posts.append(post.post_id)
#     return positive_posts
#
#
def get_posts_reacted_by_user(user_id):
    likes = PostReaction.objects.filter(user_id=user_id)
    posts_list = []
    for like in likes:
        posts_list.append(get_post(like.post_id.post_id))
    return posts_list


def get_reactions_to_post(post_id):
    likes = PostReaction.objects.filter(post_id=post_id)
    reactions = []
    for like in likes:
        post_reactions = {"user_id": like.user.id, "name": like.user.user_name,
                          "profile_pic": like.user.profile_pic, "reaction": like.reaction}
        reactions.append(post_reactions)
    return reactions


def get_reaction_metrics(post_id):
    likes = PostReaction.objects.filter(post_id=post_id)
    likes = list(likes.values('reaction'))
    reaction_count = {}
    for like in likes:
        try:
            reaction_count[like['reaction']] += 1
        except:
            reaction_count[like['reaction']] = 1
    return reaction_count


def get_total_reaction_count():
    reaction_count = PostReaction.objects.all()
    return reaction_count.count()


# def get_replies_for_comment(comment_id):
#     comment = Comments.objects.get(comment_id=comment_id)
#     replies = Comments.objects.filter(commented_on_id=comment)
#     comment_replies = []
#     for reply in replies:
#         commented_at = reply.comment_create_date
#         commented_at = ' '.join([str(commented_at.date()), str(commented_at.time())])
#         comment_reply = {"comment_id": reply.comment_id, "commenter": {
#             "user_id": reply.user_id.user_id,
#             "name": reply.user_id.user_name,
#             "profile_pic_url": reply.user_id.profile_pic
#         }, "commented_at": commented_at, "comment_content": reply.message}
#         comment_replies.append(comment_reply)
#
#     return comment_replies
#
#
def delete_post(post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
