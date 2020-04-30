from rest_framework import serializers

from .models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created',)
        model = Comment
        read_only_fields = ('author', 'post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,
                                        slug_field='username')
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    def validate(self, attr):
        following = attr.get('following')
        user = self.context['request'].user
        is_follow = Follow.objects.filter(
            user__username=user, following__username=following).exists()
        if is_follow:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.')
        return attr

    class Meta:
        fields = ('id', 'user', 'following',)
        model = Follow
