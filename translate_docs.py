import os
import re
import json
from google.cloud import translate_v2 as translate
from git import Repo
from github import Github, GithubException


def set_google_credentials():
    secret_value = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    with open('credentials.json', 'w') as f:
        json.dump(json.loads(secret_value), f)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'


def get_pull_request_number():
    github_ref = os.getenv('GITHUB_REF')
    match = re.match(r'refs/pull/(\d+)/merge', github_ref)
    return int(match.group(1)) if match else None

def translate_md_files():
    set_google_credentials()
    translate_client = translate.Client()
    target_languages = ['es']

    # Get the base branch of the pull request
    base_branch = os.getenv('GITHUB_BASE_REF', 'main')  # Default to 'main' if not available
    repo_name = os.getenv('GITHUB_REPOSITORY')

    # Initialize PyGithub
    g = Github(os.getenv('GITHUB_TOKEN'))

    # Fetch all branches from the remote repository
    repo = Repo(search_parent_directories=True)
    origin = repo.remote(name='origin')
    origin.fetch()

    # Specify the source and target language parent folders
    source_parent_folder = 'docs'
    target_parent_folder = 'docs'

    # Discover all version folders under the source parent folder
    version_folders = [f for f in os.listdir(source_parent_folder) if os.path.isdir(os.path.join(source_parent_folder, f))]
 
    pull_request_number = get_pull_request_number()
    repository = g.get_repo(repo_name, lazy=False)
    pull_request = repository.get_pull(pull_request_number)
    head_branch = pull_request.head.ref
    files = pull_request.get_files()

    modified_files = {file.filename: repository.get_contents(file.filename, ref=head_branch).decoded_content.decode('utf-8') for file in files}

    for version in version_folders:
        source_language_folder = os.path.join(source_parent_folder, version, 'en')

        for target_language in target_languages:
            target_language_folder = os.path.join(target_parent_folder, version, target_language)

            if not os.path.exists(target_language_folder):
                os.makedirs(target_language_folder)

            # List all markdown files in the source language folder
            md_files = [os.path.join(source_language_folder, f) for f in os.listdir(source_language_folder) if f.endswith('.md')]

            for md_file in md_files:
                content = modified_files.get(md_file)
                if not content:
                    continue

                translated_file = os.path.join(target_language_folder, os.path.basename(md_file))
                translation = translate_client.translate(content, target_language=target_language, format_='text')

                with open(translated_file, 'w', encoding='utf-8') as f:
                    f.write(translation['translatedText'])

                # Commit changes to Git
                repo = Repo(search_parent_directories=True)
                branch_name = f'translate-{os.path.basename(md_file)}-{target_language}'
                repo.git.checkout(base_branch)
                repo.git.checkout('-b', branch_name)
                repo.index.add([translated_file])
                commit_message = f'Translate {os.path.basename(md_file)} to {target_language}'
                repo.index.commit(commit_message)
                origin = repo.remote(name='origin')
                origin.push(branch_name)

                # Create pull request
                repo = g.get_repo(repo_name)
                title = f'Translate {os.path.basename(md_file)} to {target_language}'
                body = f'This pull request translates {os.path.basename(md_file)} to {target_language}'
                try:
                    repo.create_pull(title=title, body=body, head=branch_name, base=base_branch)
                except GithubException as e:
                    print(f"Failed to create pull request for {md_file}: {e}")


if __name__ == "__main__":
    translate_md_files()
