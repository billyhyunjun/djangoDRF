from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from articles.models import Article, Comment
from articles.serializers import (
    ArticleSerializer, CommentSerializer, ArticleDetailSerializer,)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# 함수형
# @api_view(["GET", "POST"])  # 함수형 drf호출시에는 api_view 필수로 데코레이터 !
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)  # 데이터 직렬화 복수는 many
#         return Response(serializer.data)  # 직렬화 한 데이터 송출
#     elif request.method == "POST":
#         # 데이터를 가져오면서 바로 직렬화를 할 수 있습니다/
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):  # 데이터 유효성 검사
#             # >>>>>>>>>>>>>>>> raise_exception=True를 적으면 오른쪽과 같은 결과를 보내줌 return Response(serializer.errors, status=400)  # 유효성 실패시 오류 내용 및 상태 400으로 전송
#             serializer.save()  # db저장
#             # 결과 송출 및 상태 201 = create로 보내줌 기본값은 200
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET","DELETE", "PUT"])
# def article_detail(request, pk):
#     if request.method == "GET":
#         article = get_object_or_404(Article, pk=pk)
#         print(article)  # 해당 pk가 있다면 가져오고 없다면 404에러
#         serializer = ArticleSerializer(article)  # 단수는 many 없음
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         article = get_object_or_404(Article, pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == "PUT":
#         article = get_object_or_404(Article, pk=pk)
#         # 기존 form양식에서는 (수정 데이터, 찾아올 조건)이 였지만, 여기는 (찾아올 데이터, 수정 데이터)로 넣어준다.
#         serializer = ArticleSerializer(article, data=request.data, partial=True) # partial=True 일부분 수정 가능 변경
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)


# 클레스형
class ArticleListAPIView(APIView):

    permission_classes = [IsAuthenticated]  # 토큰이 있을 때에만 가능

    @extend_schema(
        tags=["Articles"],
        description="Article 목록 조회를 위한 API",
    )
    def get(self, request):
        # <<<< request.user 하면 유저 정보 가져오는것도 가능!>>>>
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)  # 데이터 직렬화 복수는 many
        return Response(serializer.data)

    @extend_schema(
        tags=["Articles"],
        description="Article 생성를 위한 API",
        request=ArticleSerializer,
    )
    def post(self, request):
        # 데이터를 가져오면서 바로 직렬화를 할 수 있습니다/
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # 데이터 유효성 검사
            # >>>>>>>>>>>>>>>> raise_exception=True를 적으면 오른쪽과 같은 결과를 보내줌 return Response(serializer.errors, status=400)  # 유효성 실패시 오류 내용 및 상태 400으로 전송
            serializer.save()  # db저장
            # 결과 송출 및 상태 201 = create로 보내줌 기본값은 200
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)  # 반복되는 내용은 하나의 함수로 정의

    def get(self, request, pk):
        article = self.get_object(pk)  # 위에 함수에서 가져와서 쓸수 있음
        serializer = ArticleDetailSerializer(article)  # 단수는 many 없음
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        # 기존 form양식에서는 (수정 데이터, 찾아올 조건)이 였지만, 여기는 (찾아올 데이터, 수정 데이터)로 넣어준다.
        serializer = ArticleDetailSerializer(
            article, data=request.data, partial=True)  # partial=True 일부분 수정 가능 변경
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = CommentSerializer(data=request.data)
        # └> article 필드가 채워지지 않아서 자꾸 유효성에서 탈락이 된다면? read_only_fields = ("article",)를 생각해보자
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)  # 기존 데이터에서 맞는 아티클 데이터를 찾아서 넣어준다.
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def check_sql(request):
    from django.db import connection

    comments = Comment.objects.all().select_related("article")
    for comment in comments:
        print(comment.article.title)

    articles = Article.objects.all().prefetch_related("comments")
    for article in articles:
        comments = article.comments.all()
        for comment in comments:
            print(comment.content)

    print("-" * 30)
    print(connection.queries)

    return Response()
