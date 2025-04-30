from setuptools import setup, find_packages

setup(
    name="dm_jira_validator",
    version="0.12.0",
    author="Brigitte Mendez",
    author_email="mendezbrigitte13@gmail.com",
    description="Un validador de tickets de Jira que verifica atributos y subtareas.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BrigitteMendez1302/jira-ticket-validator",
    packages=find_packages(),
    install_requires=[
        "jira",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "dm-jira-validator=dm_jira_validator:validate_ticket",
        ],
    },
)