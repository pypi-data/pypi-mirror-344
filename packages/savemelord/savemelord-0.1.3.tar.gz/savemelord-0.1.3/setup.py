from setuptools import setup, find_packages

setup(
    name='savemelord',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,  # <<< THIS IS VERY IMPORTANT
    package_data={
        'savemelord': ['gridworld.txt'],  # <<< Tells it to include gridworld.txt
    },
    description='My cool package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
