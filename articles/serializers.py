from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article",)  # 읽기만 하고 넣을 때는 따로 넣어주겠다..
        
    # 만약에 serializer 안에 필요 없는 필드를 빼고 보여 주고 싶다면??
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(ArticleSerializer):
        # 위에 선언된 Comment를 끌어다가(comments 역참조) 가져와서 사용을 할 수 있게 할 수 있다. read_only=True를 하는 이유는 post될 때에 쓰기하는 것을 방지하기 위해
    comments = CommentSerializer(many=True, read_only=True)
    # source를 이용하여 해당 필드를 채우는 속성을 지정할 수 있으며, .count등으로 속성접근가능
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)