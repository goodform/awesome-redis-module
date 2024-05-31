import subprocess
import os
from datetime import datetime

# Get the license information and category of a repository
def get_repository_license(remote_url):
    # Analyze the license category
    license_type = "Unknown license"

    # Clone the repository
    try:
        subprocess.call(['git', 'clone', '--quiet', '--depth', '1', remote_url])
    except subprocess.CalledProcessError:
        print("Failed to clone the repository.")
        return

    # Change to the repository directory
    repo_name = os.path.basename(remote_url).split('.')[0]
    os.chdir(repo_name)

    # Get the license file names
    license_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.startswith('LICENSE') or file.startswith('LICENCE') or file.startswith('COPYING'):
                license_files.append(os.path.join(root, file))

    # Get the license content and category
    if license_files:
        for license_file in license_files:
            with open(license_file, 'r') as f:
                license_content = f.read()

            if 'MIT License' in license_content:
                license_type = "MIT License"
            elif 'Apache License' in license_content:
                license_type = "Apache License"
            elif 'BSD 3-Clause License' in license_content:
                license_type = "BSD 3-Clause License"
            elif 'Redis Source Available License 2.0' in license_content:
                license_type = "Redis Source Available License 2.0"
            elif 'Redis Source Available License' in license_content:
                license_type = "Redis Source Available License"
            elif 'GNU General Public License' in license_content:
                license_type = "GNU GPL"
    else:
        print("No license files found.")

    # Get the last commit time
    try:
        last_commit_time = subprocess.check_output(['git', 'log', '-1', '--format=%cd', '--date=format:%Y-%m-%d %H:%M:%S']).decode().strip()
    except subprocess.CalledProcessError:
        print("Failed to get the last commit time.")

    # Output the repository information (in the format "username/repository")
    repo_info = "[" + "/".join(remote_url.split('/')[-2:]) + "]" + "(" + remote_url + ")"
    return [repo_info, license_type, last_commit_time]

def print_markdown_table(headers, data):
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "|-" + "-|".join(['-' * len(header) for header in headers]) + "-|"

    data_lines = []
    for row in data:
        data_line = "| " + " | ".join(str(cell) for cell in row) + " |"
        data_lines.append(data_line)

    print(header_line)
    print(separator_line)
    for line in data_lines:
        print(line)

def sort_by_third_column(row):
    time_str = row[2]
    datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return datetime_obj

file_path = "libraries.txt"
if not os.path.isfile(file_path):
    print("file " + file_path + " not exist")

# Create a "tmp" directory if it doesn't exist
tmp_dir = "tmp"
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

with open(file_path, 'r') as file:
    # Change to the "tmp" directory
    os.chdir(tmp_dir)
    current_dir = os.getcwd()
    
    headers = ["Repo", "License", "Last Commit Time"]
    table_data = []

    lines = file.readlines()
    for line in lines:
        os.chdir(current_dir)
        # Call the function with the path to the Git repository for analysis
        res = get_repository_license(line.strip())
        table_data.append(res)
    table_data = sorted(table_data, key=sort_by_third_column, reverse=True)
    print_markdown_table(headers, table_data)