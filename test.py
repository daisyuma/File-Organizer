import unittest
from download_file_handler import DownloadFileHandler

class TestFileHandler(unittest.TestCase):
    file_handler = DownloadFileHandler(file_path='/Users/daisyma/Downloads', threshold=0)

    def test_check_file(self):
        result = self.file_handler.check_file("", "")
        # self.assertTrue(result)
        print(result)

if __name__ == '__main__':
    unittest.main()