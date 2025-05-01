from setuptools import setup, find_packages

setup(
    name="ab-agents",  # Your package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.4.1",  # Gemini API
        "python-dotenv>=1.0.0",         # To load environment variables
        "requests>=2.25.0",        
    ],
    author="Abu Bakar",
    author_email="abubakarbinzohaib@gmail.om",
    description="A powerful agent SDK for easy creation and integration",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/abubakarzohaib141/ab_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
