from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username', read_only=False
    )

    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        follow = data['following']
        if user == follow:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя")
        if Follow.objects.filter(
            user=user,
            following=follow
        ).exists():

            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора"
            )
        return data
