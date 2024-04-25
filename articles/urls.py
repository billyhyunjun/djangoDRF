from django.urls import path
from . import views


app_name = "articles"
urlpatterns = [
    path("", views.ArticleListAPIView.as_view(),
         name="article_list"),  # 클래스 함수 호출 방법 클래스명.as_view()
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:article_pk>/comments/",
         views.CommentListAPIView.as_view(), name="comment_list"),
    path("comments/<int:comment_pk>/",
         views.CommentDeleteAPIView.as_view(), name="comment_delete"),
     path("check_sql/", views.check_sql, name="check_sql"),
]
