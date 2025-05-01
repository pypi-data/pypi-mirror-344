from setuptools import setup, find_packages

setup(
    name='guiphyton',
    version='1.0.0',
    description='A fully custom console UI toolkit without tkinter or graphics!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ruzgar',
    author_email='ruzgartvtr@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
