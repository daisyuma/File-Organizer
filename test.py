import unittest
import shutil
import os
from download_file_handler import DownloadFileHandler
from pathlib import Path

class TestFileHandler(unittest.TestCase):
    file_handler = DownloadFileHandler(file_path='/Users/daisyma/Downloads/', threshold=80)

    # def test_check_similarity(self):
    #     result = self.file_handler.check_similarity("phil fileAutomator (3)", " math fileAutomator (4)")
    #     # self.assertTrue(result)
    #     print(result)
    
    # def test_get_similar_files(self):
    #     result = self.file_handler.get_similar_files("fileAutomator (6).py")

    # def test_get_filename(self):
    #     result = self.file_handler.get_filename("/Users/daisyma/Downloads/fileAutomator (6).py")

    def test_read_folders(self):
        result = self.file_handler.read_folders()
    
    # def test_get_keyword(self):
    #     filenames = self.file_handler.get_similar_files("fileAutomator (6).py")
    #     keyword = self.file_handler.get_keyword(filenames)
    #     self.assertEqual("fileAutomator", keyword)
    
    def test_is_folder_created(self):
        #Arrange.
        test_folder_name = "Test_folderA"
        #create test folder
        Path("/Users/daisyma/Downloads/" + test_folder_name).mkdir(parents=True, exist_ok=True) 
        #create some test files
        for i in range(1,5):
            with open("/Users/daisyma/Downloads/" + test_folder_name + "/" + test_folder_name + str(i) + ".txt", 'w') as fp:
                fp.write('test test test')
        
        #Act.
        result = self.file_handler.is_folder_created(test_folder_name)

        #Assert.
        self.assertEqual(test_folder_name, result)

        #Cleanup
        shutil.rmtree("/Users/daisyma/Downloads/" + test_folder_name)
    

    def test_create_folder(self):
        #Arrange.
        folder_name = "test_create_folder"
        #Act.
        self.file_handler.create_folder(folder_name)
        #Assert.
        self.assertTrue(os.path.isdir("/Users/daisyma/Downloads/Test_create_folder"))
        #Cleanup
        shutil.rmtree("/Users/daisyma/Downloads/Test_create_folder")
    
    def test_move_files(self):
        #Arrange.
        test_folder_path = "/Users/daisyma/Downloads/Test_folderA/"
        test_file_name = "test_move_file"
        #create test folder
        Path(test_folder_path).mkdir(parents=True, exist_ok=True) 
        #create some test files in Downloads
        file_entries = []
        for i in range(1,5):
            file_path = self.file_handler.file_path + test_file_name + str(i) + ".txt"
            with open(file_path, 'w') as fp:
                fp.write('test test test')
            file_entries.append(file_path)
        #Act.
        self.file_handler.move_files(file_entries, test_folder_path)
        #Assert.
        self.assertTrue(os.path.isfile("/Users/daisyma/Downloads/Test_folderA/" + test_file_name + "4.txt"))
        #Cleanup.
        shutil.rmtree(test_folder_path)

                

if __name__ == '__main__':
    unittest.main()