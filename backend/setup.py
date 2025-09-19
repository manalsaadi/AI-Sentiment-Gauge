from setuptools import setup, find_packages

setup(
    name="ai-sentiment-gauge",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.4.0",
        "python-multipart>=0.0.6",
        "argostranslate>=1.9.0",
        "beautifulsoup4>=4.9.3",
        "requests>=2.26.0",
        "nltk>=3.6.5",
        "scikit-learn>=0.24.2",
        "pandas>=1.3.3",
        "numpy>=1.21.2",
        "markdown>=3.3.4",
        "emoji>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.1",
            "pytest-asyncio>=0.23.0",
            "httpx>=0.24.0",
            "mypy>=0.910",
            "black>=21.9b0",
            "flake8>=3.9.2",
            "isort>=5.9.3",
        ],
    },
)