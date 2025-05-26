from rest_framework import serializers

from blogs.models import Blog


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    tagline = serializers.CharField()

    def create(self, validated_data): # Create and return a new `Blog` instance, given the validated data.
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data): # Update and return an existing `Blog` instance, given the validated data.
        instance.name = validated_data.get('name', instance.name)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.save()
        return instance