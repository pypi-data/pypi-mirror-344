from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm_jailbreak",
    version="0.1.1",
    author="Jay Woden", 
    author_email="wodenjay@gmail.com",
    description="A jailbreak package which integration some open manners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.1",
        "transformers>=4.28.0",
        "numpy>=1.26.0",
        "tqdm>=4.66.1",
        "accelerate>=0.23.0",
        "openai>=1.12.0",
        "nltk>=3.8.1",
        "sentencepiece>=0.1.99",
        "protobuf>=4.24.4"
    ],
    include_package_data=True,
    package_data={
        "autodan": [
            "data/advbench/*",
            "assets/*"
        ]
    },
    entry_points={
        "console_scripts": [
            "autodan=autodan.core:AutoDAN.run",
        ],
    },
)
