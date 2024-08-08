from collections import OrderedDict

from django.test import TestCase

from api.models import TestFilePath, TestEnvironment
from api.usecases import get_assets


class TestGetAssets(TestCase):
    def setUp(self) -> None:
        TestFilePath.objects.all().delete()
        TestEnvironment.objects.all().delete()

    def test_empty_models(self):
        self.assertEqual(
            {'available_paths': [], 'test_envs': [], 'upload_dirs': []},
            get_assets()
        )

    def test_models_data_initialized(self):
        path = TestFilePath.objects.create(path='path/to/file.txt')
        env = TestEnvironment.objects.create(name='env1')
        path_dict = OrderedDict([('id', path.id), ('path', path.path)])
        env_dict = OrderedDict([('id', env.id), ('name', env.name)])
        env_dirs = ["path/to"]
        data = get_assets()
        self.assertIn('available_paths', data)
        self.assertIn('test_envs', data)
        self.assertIn('upload_dirs', data)
        self.assertEqual(1, len(data['available_paths']))
        self.assertEqual(1, len(data['test_envs']))
        self.assertEqual(1, len(data['upload_dirs']))
        self.assertEqual(path_dict, data['available_paths'][0])
        self.assertEqual(env_dict, data['test_envs'][0])
        self.assertEqual(env_dirs, data['upload_dirs'])
