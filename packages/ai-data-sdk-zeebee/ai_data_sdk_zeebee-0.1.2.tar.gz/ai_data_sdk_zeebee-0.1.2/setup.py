from setuptools import setup, find_packages

# Read the long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ai-data-sdk-zeebee",
    version="0.1.2",
    description="A comprehensive SDK for interacting with AI Data SDK API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zeebee Team",
    author_email="info@zeebee.com",
    url="https://github.com/zeebee/ai-data-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "numpy>=1.20.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    keywords=["ai", "data", "embeddings", "vector database", "pii"],
)
