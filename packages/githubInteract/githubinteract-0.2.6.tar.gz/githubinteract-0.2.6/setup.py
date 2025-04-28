
from setuptools import setup, find_packages
with open("README.md", "r") as fh: 
    long_description = fh.read() 

setup(
    name='githubInteract',
    version='0.2.6',
    author='Brigham Turner',
    author_email='brighamturner@narratebay.com',
    description='''
This package allows users to interact with github from python.
I created it to simplify using github: many things i wish I could do in github with one command actually require several commands.
For example: uploading an entire folder (which beforehand wasn't initiated into github) to a repo is one command: (the function uploadFolderFileAsCommitToRepo). In normal git this would have been surprisingly complicated: first you would need to initiate the folder, but to initiate the folder you would need to pull from the original github repo, but that would then wipe all the contents of that folder or require a merging procedure.
Additionally, pushing usually requires 3 steps: 1) adding, committing, and pushing. This now makes it be only one step (again the function uploadFolderFileAsCommitToRepo).
Ultimately, there is a reason why github is so complex: it is intended to allow multiple users to work on the same project - but when you are just a single user this complexity is burdensome.
''',
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    packages=find_packages(),
    install_requires=["github","git"], 
    license="MIT",
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)