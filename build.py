import os

commit_message = input()
os.system("git add .")
os.system(f'git commit -m "{commit_message}"')
os.system("git push")
os.system("docker build --tag fansic .")
os.system("docker push cooljosh0221/fansic")
