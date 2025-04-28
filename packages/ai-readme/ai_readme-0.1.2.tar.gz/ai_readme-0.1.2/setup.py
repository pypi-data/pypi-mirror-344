from setuptools import setup, find_packages

setup(
    name="ai-readme",
    version="0.1.2",
    author="JoeyKim",
    author_email="hyoj0492@gmail.com",
    description="Automatically generate README.md using AI.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hyoj0942/ai-readme",
    packages=find_packages(),
    install_requires=[
        "openai",
        "anthropic",
        "google-generativeai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "readme=readme_generator.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
