from .models import User, Post, CommentReaction, Comment, PostReaction
from django.utils import timezone as t
from django.db.models import Q, F, Count


def get_user_data(obj):
    user = {
        "user_id": obj.user_id,
        "name": obj.user.user_name,
        "profile_pic_url": obj.user.profile_pic
    }
    return user


def get_comment_data(comment):
    commenter = get_user_data(comment)
    commented_at = comment.comment_create_date
    commented_at = commented_at.strftime("%Y-%m-%d %H:%M:%S")
    reaction = CommentReaction.objects.filter(id=comment.id).values('reaction')
    reaction_count = reaction.count()
    reactions = [like.reaction for like in reaction]
    comment_reactions = {"count": reaction_count, "type": reactions}
    post_comment = {"comment_id": comment.id, "commenter": commenter, "commented_at": commented_at,
                    "comment_content": comment.message, "reactions": comment_reactions,
                    }
    return post_comment


def get_reply_data(reply):
    replied_at = reply.comment_create_date
    replied_at = replied_at.strftime("%Y-%m-%d %H:%M:%S")
    reply_data = {
        "comment_id": reply.id,
        "commenter": get_user_data(reply),
        "commented_at": replied_at,
        "comment_content": reply.message
    }
    return reply_data


def get_post(post_id):
    post = Post.objects.get(id=post_id)
    posted_by = get_user_data(post)
    posted_at = post.post_created_date
    posted_at = posted_at.strftime("%Y-%m-%d %H:%M:%S")
    post_content = post.post_description
    post_likes = PostReaction.objects.filter(post_id=post_id).values('reaction').distinct()
    post_reactions = [like['reaction'] for like in post_likes]
    comments = Comment.objects.filter(post_id=post_id, commented_on_id=None)
    comments_count = comments.count()
    post_comments = []
    for comment in comments:
        post_replies = []
        replies = Comment.objects.filter(post_id=post_id, commented_on_id=comment.id)
        replies_count = replies.count()
        for reply in replies:
            reply_reaction = CommentReaction.objects.filter(comment_id=reply.id).values('reaction')
            reply_react_count = reply_reaction.count()
            reply_react_type = [like.reaction for like in reply_reaction]
            replier = get_reply_data(reply)
            replier["reactions"] = {"count": reply_react_count, "type": reply_react_type}
            post_replies.append(replier)
        post_comment = get_comment_data(comment)
        post_comment["replies_count"] = replies_count
        post_comment["replies"] = post_replies
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


def get_posts_with_more_positive_reactions():
    positive_posts = PostReaction.objects.values('post').annotate(positive_count=Count('reaction', filter=Q(reaction__in=("LIKE", "LOVE", "WOW", "HAHA"))), negative_count=Count('reaction', filter=Q(reaction__in=("SAD", "ANGRY")))).filter(positive_count__gt=F('negative_count')).values('post_id')
    return list(positive_posts)


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
        post_reactions = get_user_data(like)
        post_reactions["reaction"] = like.reaction
        reactions.append(post_reactions)
    return reactions


def get_reaction_metrics(post_id):
    likes = PostReaction.objects.filter(post_id=post_id).values('reaction').annotate(react_count=Count('reaction'))
    reaction_count = {like['reaction']: like['react_count'] for like in likes}
    return reaction_count


def get_total_reaction_count():
    reaction_count = PostReaction.objects.all()
    return reaction_count.count()


def get_replies_for_comment(comment_id):
    replies = Comment.objects.filter(commented_on_id=comment_id)
    if replies.count() == 0:
        return "Bad Request"
    comment_replies = []
    for reply in replies:
        comment_reply = get_reply_data(reply)
        comment_replies.append(comment_reply)

    return comment_replies


def delete_post(post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
