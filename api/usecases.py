from api.models import TestFilePath, TestEnvironment
from api.serializers import TestFilePathSerializer, TestEnvironmentSerializer, TestUploadDirSerializer


def get_assets():
    upload_dirs_list = list(set([item.upload_dir for item in TestFilePath.objects.all().order_by("path")]))
    return {
        'available_paths': TestFilePathSerializer(TestFilePath.objects.all().order_by('path'), many=True).data,
        'test_envs': TestEnvironmentSerializer(TestEnvironment.objects.all().order_by('name'), many=True).data,
        "upload_dirs": upload_dirs_list,
    }
