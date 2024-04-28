#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""
import unittest
import json
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up for the test"""
        self.storage = FileStorage()
        self.obj = BaseModel()

    def tearDown(self):
        """Clean the file storage"""
        try:
            os.remove(FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def test_all(self):
        """Test the all method"""
        all_objs = self.storage.all()
        self.assertEqual(type(all_objs), dict)
        self.assertEqual(all_objs, self.storage._FileStorage__objects)

    def test_new(self):
        """Test the new method"""
        self.storage.new(self.obj)
        key = "{}.{}".format(self.obj.__class__.__name__, self.obj.id)
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_save(self):
        """Test the save method"""
        self.storage.new(self.obj)
        self.storage.save()
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            saved_data = json.load(f)
        key = "{}.{}".format(self.obj.__class__.__name__, self.obj.id)
        self.assertIn(key, saved_data)

    def test_reload(self):
        """Test the reload method"""
        self.storage.new(self.obj)
        self.storage.save()
        del self.storage
        new_storage = FileStorage()
        new_storage.reload()
        key = "{}.{}".format(self.obj.__class__.__name__, self.obj.id)
        self.assertIn(key, new_storage._FileStorage__objects)

    def test_delete(self):
        """Test the delete method"""
        self.storage.new(self.obj)
        self.storage.save()
        self.storage.delete(self.obj)
        self.assertNotIn(self.obj, self.storage._FileStorage__objects.values())

    def test_get(self):
        """Test the get method"""
        self.storage.new(self.obj)
        self.storage.save()
        self.assertEqual(self.storage.get(type(self.obj), self.obj.id), self.obj)

    def test_count(self):
        """Test the count method"""
        self.assertEqual(self.storage.count(type(self.obj)), 0)
        self.storage.new(self.obj)
        self.storage.save()
        self.assertEqual(self.storage.count(type(self.obj)), 1)

if __name__ == "__main__":
    unittest.main()
