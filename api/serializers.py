import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import serializers

from api.models import TestRunRequest, TestFilePath, TestEnvironment


class TestRunRequestSerializer(serializers.ModelSerializer):
    env_name = serializers.ReadOnlyField(source='env.name')

    class Meta:
        model = TestRunRequest
        fields = (
            'id',
            'requested_by',
            'env',
            'path',
            'status',
            'created_at',
            'env_name'
        )
        read_only_fields = (
            'id',
            'created_at',
            'status',
            'logs',
            'env_name'
        )


class TestRunRequestItemSerializer(serializers.ModelSerializer):
    env_name = serializers.ReadOnlyField(source='env.name')

    class Meta:
        model = TestRunRequest
        fields = (
            'id',
            'requested_by',
            'env',
            'path',
            'status',
            'created_at',
            'env_name',
            'logs'
        )


class TestFilePathSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestFilePath
        fields = ('id', 'path')


class TestEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEnvironment
        fields = ('id', 'name')


class TestUploadDirSerializer(serializers.ModelSerializer):
    upload_dir = serializers.CharField()

    class Meta:
        model = TestFilePath
        fields = ('upload_dir', )


class TestFileUploadSerializer(serializers.Serializer):
    upload_dir = serializers.CharField(required=True)
    test_file = serializers.FileField(write_only=True, required=True)

    def save(self, **kwargs):
        test_file = self.validated_data['test_file']
        upload_dir = self.validated_data['upload_dir']
        full_file_path = os.path.join(upload_dir, test_file.name)
        default_storage.save(full_file_path, ContentFile(test_file.read()))
        obj = TestFilePath.objects.create(path=full_file_path)
        return obj



