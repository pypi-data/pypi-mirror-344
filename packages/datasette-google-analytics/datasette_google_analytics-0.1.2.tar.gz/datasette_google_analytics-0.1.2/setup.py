from setuptools import setup
import os

__version__ = "0.1.2"


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
    ],
    version=__version__,
    python_requires=">=3.9",
    packages=["datasette_google_analytics"],
    package_data={"datasette_google_analytics": ["templates/*.html"]},
    entry_points={"datasette": ["google_analytics = datasette_google_analytics"]},
    install_requires=["datasette>=0.54"],
    extras_require={
        "test": [
            "beautifulsoup4",
            "pytest-asyncio",
            "pytest",
            "python-semantic-release",
        ]
    },
)
