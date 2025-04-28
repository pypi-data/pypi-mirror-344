
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jwt_manager",
    version="0.1.0",
    author="Faizan Utilities",
    author_email="support@example.com",
    description="A lightweight utility to create, validate, and refresh JWT tokens easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_github_username/jwt_manager",
    project_urls={
        "Bug Tracker": "https://github.com/your_github_username/jwt_manager/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["PyJWT"],
)
