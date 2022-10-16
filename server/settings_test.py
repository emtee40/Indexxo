import json
import pathlib
import shutil
import unittest
import tempfile
from server.settings import IndexxoSettings


class SettingsTest(unittest.TestCase):
    temp_dir: tempfile.TemporaryDirectory
    temp_dir_path: pathlib.Path

    @classmethod
    def setUp(cls):
        """
        Creates temporary directory and creates database with dummy data in it.
        Also changes current date, so results will not be affected by date.
        """
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.temp_dir_path = pathlib.Path(cls.temp_dir.name)
        print(cls.temp_dir)
        print("testdir created", cls.temp_dir.name)

    @classmethod
    def tearDown(cls):
        """
        Deletes temporary directory with database
        """
        print('Deleting temporary directory...')
        cls.temp_dir.cleanup()
        print("Temporary directory was deleted")

    def test_load_config_file_no_file_no_folder(self):
        """
        Test loading config.json file when there is no such file
        and no folder called "indexxo". Freshly installed app.
        """
        settings = IndexxoSettings(indexxo_directory=self.temp_dir_path)

        # Now loading file, this must create a new config.json file with default settings
        settings.load_config_file()
        config: dict = json.load(open(settings.config_path))
        print("Config file here", settings.config_path)
        self.assertEqual(
            config,
            {'space_paths': [], 'ignore_paths': [], 'update_interval': 3600}
        )

    def test_load_config_file_no_file(self):
        """
        Test loading config.json file when there is no such file
        but there is a folder called "indexxo". Missing config.json.
        """
        settings = IndexxoSettings(indexxo_directory=self.temp_dir_path)

        # Now loading file, this must create a new config.json file with default settings
        settings.load_config_file()
        config: dict = json.load(open(settings.config_path))
        self.assertEqual(
            config,
            {'space_paths': [], 'ignore_paths': [], 'update_interval': 3600}
        )

    def test_load_config_file_ok(self):
        """
        Loading config file when it exists and valid
        """
        settings = IndexxoSettings(indexxo_directory=self.temp_dir_path)

        # Writing settings before loading them from file
        settings_data = {
            "space_paths": ['/folder1/subfolder', '/folder2/subfolder'],
            "ignore_paths": ['/folder3/subfolder', '/folder4/subfolder'],
            "update_interval": 2800
        }
        json.dump(settings_data, open(settings.config_path, 'w'))

        # Now loading file, this must use existing config.json file
        settings.load_config_file()
        self.assertEqual(['/folder1/subfolder', '/folder2/subfolder'], settings.space_paths)
        self.assertEqual(['/folder3/subfolder', '/folder4/subfolder'], settings.ignore_paths)
        self.assertEqual(2800, settings.update_interval)

    def test_update_config_file(self):
        """
        Update config file when it exists and valid
        """
        settings = IndexxoSettings(indexxo_directory=self.temp_dir_path)

        # Writing settings before loading them from file
        settings_data = {
            "space_paths": ['/folder1/subfolder', '/folder2/subfolder'],
            "ignore_paths": ['/folder3/subfolder', '/folder4/subfolder'],
            "update_interval": 2800
        }
        with open(self.temp_dir_path / "dummy.json", 'w') as f:
            json.dump(settings_data, open(self.temp_dir_path / "dummy.json", 'w'))
            settings.update_config_file(open(self.temp_dir_path / "dummy.json"))
        # Now checking if config has been updated
        self.assertEqual(['/folder1/subfolder', '/folder2/subfolder'], settings.space_paths)
        self.assertEqual(['/folder3/subfolder', '/folder4/subfolder'], settings.ignore_paths)
        self.assertEqual(2800, settings.update_interval)

if __name__ == '__main__':
    unittest.main(
        failfast=False,
        catchbreak=False
    )
