import unittest
from download_file_handler import DownloadFileHandler

class TestFileHandler(unittest.TestCase):
    file_handler = DownloadFileHandler(file_path='/Users/daisyma/Downloads/', threshold=90)

    # def test_check_file(self):
    #     result = self.file_handler.check_file("phil fileAutomator (3)", " math fileAutomator (4)")
    #     # self.assertTrue(result)
    #     print(result)
    
    # def test_get_similar_files(self):
    #     result = self.file_handler.get_similar_files("/Users/daisyma/Downloads/fileAutomator (6).py")

    def test_get_filename(self):
        result = self.file_handler.get_filename("/Users/daisyma/Downloads/fileAutomator (6).py")

if __name__ == '__main__':
    unittest.main()