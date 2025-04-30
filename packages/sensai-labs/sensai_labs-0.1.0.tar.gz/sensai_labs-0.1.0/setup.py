from setuptools import find_namespace_packages, setup

setup(
    name="sensai-labs",
    version="0.1.0",
    description="AI Agents for Hardware",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="yudhisteer",
    author_email="yudhisteer@gmail.com",
    url="https://github.com/sensai-ai",
    package_dir={"": "."},
    packages=find_namespace_packages(
        where=".", include=["client.*", "shared.*", "client.agents.*"]
    ),
    python_requires=">=3.12",
    install_requires=[
        "black>=25.1.0",
        "colorlog>=6.9.0",
        "decouple>=0.0.7",
        "fastapi>=0.115.12",
        "isort>=6.0.1",
        "mcp[cli]>=0.1.0",
        "openai>=1.69.0",
        "psycopg2>=2.9.10",
        "pydantic>=2.11.0",
        "requests>=2.32.3",
        "setuptools>=78.1.0",
        "supabase>=2.15.0",
        "uvicorn>=0.34.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    project_urls={
        "Source": "https://github.com/sensai-ai",
        "Bug Tracker": "https://github.com/sensai-ai/issues",
    },
)
