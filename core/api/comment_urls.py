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


"""
/coments/pk - get comment and return in this fmt and return 404 if live=false
{
    "id": 1, # pk
    "body": "This is a comment",
    "author": 3 # id 
    "children": [1, 32, 45] # list of ids
    "created_at": "2020-01-01T00:00:00Z"
    "last_modified" "2020-01-01T00:00:00Z"
    "likes": 32
}

/(blog/announcements)/pk/comments - get comments and return kv pairs where k = ID and v signifies if it's a top lvl comment (only return live=true's)

{
    [
        212: True, 
        2121: False...
    [
}


/comments/<int:pk>/replies 
returnds essentially what /comments/<int:pk> returns but as a list 
    
"""
