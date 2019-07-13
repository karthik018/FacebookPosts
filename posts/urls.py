from django.urls import path, include
from posts import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/create-post/', views.CreatePost.as_view()),
    path('api/users/', views.CreateUser.as_view()),
    path('api/posts/<int:pk>', views.GetPost.as_view()),
    path('api/posts/', views.PostList.as_view()),
    path('api/comments/<int:pk>', views.CreateComment.as_view()),
    path('api/post-react/<int:pk>', views.PostReact.as_view()),
    path('api/comment-react/<int:pk>', views.CommentReact.as_view()),
    path('api/my-posts/', views.GetUserPost.as_view()),
    path('api/positive-posts/', views.GetPositivePosts.as_view()),
    path('api/posts-reacted/', views.GetPostsReactedByUser.as_view()),
    path('api/post-reactions/<int:pk>', views.GetReactionToPost.as_view()),
    path('api/post-reaction-metrics/<int:pk>', views.GetReactionMetrics.as_view()),
    path('api/reaction-count/', views.GetTotalReactionCount.as_view()),
    path('api/replies/', views.GetRepliesToComment.as_view()),
    path('api/delete-post/', views.DeletePost.as_view()),
    path('api/reply-comment/', views.ReplyToComment.as_view()),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
