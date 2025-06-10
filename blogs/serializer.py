from rest_framework import serializers

from blogs.models import Blog


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    tagline = serializers.CharField()

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.save()

        return instance


