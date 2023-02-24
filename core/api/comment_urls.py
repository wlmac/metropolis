from django.urls import path

comment_urls = [
    path(
        "comments/<int:pk>/replies",
        CommentReplies.as_view(),
        name="api_comment_replies",
    ),
    path("comment/<int:pk>", CommentDetail.as_view(), name="api_comment_detail"),
    path(
        "announcements/<int:pk>/comments",
        AnnouncementComments.as_view(),
        name="api_announcement_comments",
    ),
    path(
        "blog/<int:pk>/comments",
        BlogComments.as_view(),
        name="api_announcement_comments",
    ),
]
