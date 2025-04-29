from setuptools import setup, find_packages

setup(
    name="terraform-runner",
    version="1.0.1",
    author="ctogaigenticai",
    author_email="cto@gaigentic.ai",
    description="A Terraform automation runner for AI-driven cloud deployments.",
    long_description="A Python package to automate Terraform deployment workflows for agents and cloud services.",
    long_description_content_type="text/markdown",
    url="https://github.com/monsterindian/gaigentic-infra",
    project_urls={
        "Bug Tracker": "https://github.com/monsterindian/gaigentic-infra/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)
