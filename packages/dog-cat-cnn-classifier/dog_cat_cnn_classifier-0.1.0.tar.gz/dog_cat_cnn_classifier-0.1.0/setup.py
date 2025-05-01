import setuptools
from src.cnnClassifier import __version__ 
import yaml 
config = yaml.safe_load(open("config/credentials.yaml"))

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = config["__version__"] 

REPO_NAME = "dog-cat-classifier"
AUTHOR_USER_NAME = config["username"]
SRC_REPO = "dog-cat-cnn-classifier"  # Changed to a more unique name
AUTHOR_EMAIL = config["email"] 

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A deep learning package for dog and cat image classification using CNN",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Fixed typo in parameter name
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.7',
    install_requires=[
        "tensorflow>=2.0.0",
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "scikit-learn>=0.24.0", 
        "keras>=2.4.0",
        "PyYAML>=5.4.0",
    ]
)