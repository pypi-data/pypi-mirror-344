from setuptools import setup, find_packages

setup(
    name="lineup",
    version="0.0.2",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="A tool to customize exception tracebacks to show file, line number, and code line",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/lineup",
    packages=find_packages(),
    install_requires=[

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
