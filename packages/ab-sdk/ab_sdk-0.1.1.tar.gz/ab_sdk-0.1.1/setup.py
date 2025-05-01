from setuptools import setup, find_packages

setup(
    name='ab-sdk',
    version="0.1.0",
    description='An easy-to-use SDK',
    author='Abu Bakar',
    author_email='abubakarbinzohaib@gmail.com',
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
        'pydantic',
        'python-dotenv',
    ],
    python_requires='>=3.7',
)
