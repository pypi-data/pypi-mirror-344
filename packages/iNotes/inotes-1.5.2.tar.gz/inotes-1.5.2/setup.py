from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name="iNotes",
    version="1.5.2",
    packages=find_packages(),
    install_requires=[
        "reportlab",
        "requests",
        "python-docx",
        "pdfplumber",
    ],
    entry_points={
        "console_scripts": [
            "iNotes=iNotes.__main__:main",
            "iNotes_summarize=iNotes.summarize:summarize_notes",
        ],
    },
    description="iNotes is a simple Python package that uses AI to generate  clear, concise notes from just topics or summarize long documents. It's designed to assist students, professionals, and researchers in make short notes easily.",
    long_description=description,
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    long_description_content_type="text/markdown",
    author="TejusDubey",
    license="MIT",
)