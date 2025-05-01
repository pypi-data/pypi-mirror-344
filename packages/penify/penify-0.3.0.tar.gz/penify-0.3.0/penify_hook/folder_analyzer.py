import os
from git import Repo

from penify_hook.base_analyzer import BaseAnalyzer
from .api_client import APIClient
from .file_analyzer import FileAnalyzerGenHook
from tqdm import tqdm

class FolderAnalyzerGenHook(BaseAnalyzer):
    def __init__(self, dir_path: str, api_client: APIClient):
        self.dir_path = dir_path
        super().__init__(dir_path, api_client)

    def list_all_files_in_dir(self, dir_path: str):
        """List all non-hidden files in a directory and its subdirectories.

        This function recursively traverses the specified directory and its
        subdirectories, collecting paths of all non-hidden files. It filters out
        hidden directories and files (those starting with a dot) to ensure only
        visible files are returned.

        Args:
            dir_path (str): The path to the directory whose files and subdirectory files need to be
                listed.

        Returns:
            list: A list containing the full paths of all non-hidden files within the
                specified directory and its subdirectories.
        """

        files = []
        for dirpath, dirnames, filenames in os.walk(dir_path):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for filename in filenames:
                # Construct the full file path
                full_path = os.path.join(dirpath, filename)
                files.append(full_path)
        return files

    def run(self):
        """Run the post-commit hook.

        This function processes all files in a specified directory using a
        progress bar. It lists all files, initializes a `FileAnalyzerGenHook`
        for each file, and runs it. Errors during processing of individual files
        are caught and logged, but do not stop the processing of other files. A
        progress bar is displayed indicating the number of files processed.

        Args:
            self (PostCommitHook): The instance of the post-commit hook class.
        """
        try:
            file_list = self.list_all_files_in_dir(self.dir_path)
            total_files = len(file_list)
            print(f"Processing {total_files} files in folder [{self.dir_path}]")
            
            with tqdm(total=total_files, desc="Processing files", unit="file", ncols=80, ascii=True) as pbar:
                for file_path in file_list:
                    try:
                        analyzer = FileAnalyzerGenHook(file_path, self.api_client)
                        analyzer.run()
                    except Exception as file_error:
                        print(f"Error processing file [{file_path}]: {file_error}")
                    pbar.update(1)  # Even if there is an error, move the progress bar forward
        except Exception as e:
            print(f"File [{self.dir_path}] was not processed due to error: {e}")
