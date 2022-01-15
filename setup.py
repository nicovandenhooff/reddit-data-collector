from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="reddit-data-collector",
    version="1.0.2",
    description="A Python package that is used to download posts and comments from Reddit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicovandenhooff/reddit-data-collector",
    author="Nico Van den Hooff",
    license="MIT",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
    keywords="reddit, data science, machine learning, data collection, text",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["pandas>=1.3.5", "praw>=7.5.0", "tqdm>=4.62.3"],
    project_urls={
        "Examples": "https://github.com/nicovandenhooff/reddit-data-collector/tree/main/examples",
        "Bug Reports": "https://github.com/nicovandenhooff/reddit-data-collector/issues",
        "Source": "https://github.com/nicovandenhooff/reddit-data-collector",
    },
)
