from setuptools import setup, find_packages

# setup(
#     name='savemelord',
#     version='0.1',
#     packages=find_packages(),
#     include_package_data=True,  # important!
# )

from setuptools import setup, find_packages

setup(
    name='savemelord',           # <--- Must be UNIQUE on PyPI
    version='0.1.0',                   # Follow semantic versioning
    packages=find_packages(),
    include_package_data=True,
    description='A cool package that prints text from a file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Buxnator',
    author_email='sheeeshnator4000@gmail.com',
    url='https://github.com/Ashtrobuff/rlexp',  # optional, but good
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
