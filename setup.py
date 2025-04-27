import setuptools
from setuptools import find_packages, setup
setup(
    name="news_ai",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'beautifulsoup4',
        'requests',
        'transformers',
        'flask',
        'python-dotenv',
        'tensorflow>=2.0,<3.0',
        'pytz'
    ],
)
