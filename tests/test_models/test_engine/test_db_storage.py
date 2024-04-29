#!/usr/bin/python3
"""
Contains the TestDBStorageDocs class
"""

from datetime import datetime
import inspect
import models
from models.engine.db_storage import DBStorage
import pep8
import unittest

class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_get_method_exists(self):
        """Test that DBStorage has a get method"""
        self.assertTrue(hasattr(DBStorage, "get"))
        self.assertTrue(inspect.ismethod(DBStorage.get))

    def test_get_method_docstring(self):
        """Test that DBStorage get method has docstring"""
        self.assertIsNotNone(DBStorage.get.__doc__)

    def test_count_method_exists(self):
        """Test that DBStorage has a count method"""
        self.assertTrue(hasattr(DBStorage, "count"))
        self.assertTrue(inspect.ismethod(DBStorage.count))

    def test_count_method_docstring(self):
        """Test that DBStorage count method has docstring"""
        self.assertIsNotNone(DBStorage.count.__doc__)

    # Add other test methods related to the get() and count() methods here

if __name__ == '__main__':
    unittest.main()
