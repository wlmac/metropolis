from django.urls import path

from core.api.views.comments import *

comment_urls = [
    path(
        "comments/<str:type>/<int:pk>",  # done, not FULLY tested
        CommentListAPIView.as_view(),
        name="api_comment_list",
    ),
    path(
        "comment/create/<str:type>/<int:pk>",  # type = blogpost or announcement # done.
        CommentCreateView.as_view(),
        name="api_comment_create",
    ),
    path(
        "comment/<int:pk>/replies",  # done (but not tested)
        CommentRepliesAPIView.as_view(),
        name="api_comment_replies",
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
returns essentially what /comments/<int:pk> returns but as a list 
    
"""
