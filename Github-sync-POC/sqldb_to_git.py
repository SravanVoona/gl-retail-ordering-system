from git import Repo
from Table_to_csv import Table_to_Csv

class Push_to_Git:
    Table_to_Csv.conversion()
    repo_dir = r'C:\Users\sudheer varma\Capstone-eCommerce-project\Informational' #Path to the cloned local repository
    repo = Repo(repo_dir,search_parent_directories=True)
    file_list = [
        r'C:\Users\sudheer varma\Capstone-eCommerce-project\Informational\user_to_csv.csv', 
    ] #Path to the file that is to be pushed
    commit_message = 'Updating and backing up user details.'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push()