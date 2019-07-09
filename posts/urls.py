from django.urls import path
from posts import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('create-post/', views.CreatePost.as_view()),
    path('users/', views.CreateUser.as_view()),
    path('posts/<int:pk>', views.GetPost.as_view()),
    path('posts/', views.PostList.as_view()),
    path('comments/<int:pk>', views.CreateComment.as_view()),
    path('post-react/<int:pk>', views.PostReact.as_view()),
    path('comment-react/<int:pk>', views.CommentReact.as_view()),
    path('my-posts/', views.GetUserPost.as_view()),
    path('positive-posts/', views.GetPositivePosts.as_view()),
    path('posts-reacted/', views.GetPostsReactedByUser.as_view()),
    path('post-reactions/<int:pk>', views.GetReactionToPost.as_view()),
    path('post-reaction-metrics/<int:pk>', views.GetReactionMetrics.as_view()),
    path('reaction-count/', views.GetTotalReactionCount.as_view()),
    path('replies/', views.GetRepliesToComment.as_view()),
    path('delete-post/', views.DeletePost.as_view()),
    path('reply-comment/', views.ReplyToComment.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
