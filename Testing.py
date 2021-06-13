"""
This module contains a class TestSum which tests for all the success and failure
cases of file management system
"""
import os
import unittest
from logic_server import Services

class TestSum(unittest.TestCase):
    """
    This is used for unittesting
    """
    def test_read_file(self):
        """
        there are 3 testcases and this tests for read_file.
        """
        directory = os.path.join(os.getcwd(), 'satya')
        cli = Services(os.getcwd(), directory, 'satya')
        val = [
            ['dsd.txt'],
            ['asdf.txt'],
            ['shdjv.txt']
        ]
        ex_val = [
            'file doesnot exist',
            'file doesnot exist',
            'file doesnot exist'
        ]
        result = []
        for inputval in val:
            result.append(cli.file_read(inputval[0]))
        self.assertListEqual(result, ex_val)

    def test_folder_creation(self):
        """
        thare are 2 testcases and this tests for folder_creation.
        """
        cli = Services(os.getcwd(), os.getcwd(), 'prem')
        val = [
            'Test_folder','Test_folder'
        ]
        ex_val = [
            'failed to create folder',
            'failed to create folder'
        ]
        result = []
        for inputval in val:
            result.append(cli.create_folder(inputval))
        self.assertListEqual(result, ex_val)

    

if __name__ == '__main__':
    unittest.main()
