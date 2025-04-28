from os import path

from setuptools import find_packages, setup

# Get current directory
here = path.abspath(path.dirname(__file__))


# Read requirements from requirements.txt
def get_requirements():
    requirements = []
    try:
        with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("Warning: requirements.txt not found")
    return requirements


# Read README for long description
def get_long_description():
    try:
        with open(path.join(here, "README.md"), encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


setup(
    name="minionx",
    version="0.1.0",
    description="A powerful AI agent framework for Python",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="femto",
    author_email="femtowin@gmail.com",
    license="MIT",
    url="https://github.com/femto/minion",
    packages=["minion", "minion.main", "minion.providers", "minion.schema"],
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "minion=minion.cli:app",
        ],
    },
    keywords="ai, agent, framework, llm, automation",
)
