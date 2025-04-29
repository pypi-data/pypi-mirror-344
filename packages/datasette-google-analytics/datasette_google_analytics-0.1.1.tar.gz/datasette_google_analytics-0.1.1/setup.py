from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-google-analytics",
    description="Datasette plugin that adds Google Analytics tracking code to your Datasette instance",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Jerry Ng",
    url="https://github.com/ngshiheng/datasette-google-analytics",
    project_urls={
        "Issues": "https://github.com/ngshiheng/datasette-google-analytics/issues",
        "CI": "https://github.com/ngshiheng/datasette-google-analytics/actions",
        "Changelog": "https://github.com/ngshiheng/datasette-google-analytics/releases",
    },
    license="MIT",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: MIT License",
    ],
    version=VERSION,
    python_requires=">=3.9",
    packages=["datasette_google_analytics"],
    entry_points={"datasette": ["google_analytics = datasette_google_analytics"]},
    install_requires=["datasette>=0.54"],
    extras_require={
        "test": [
            "beautifulsoup4",
            "pytest-asyncio",
            "pytest",
            "python-semantic-release",
        ],
        "build": [
            "wheel",
            "build",
            "setuptools",
        ],
    },
)
