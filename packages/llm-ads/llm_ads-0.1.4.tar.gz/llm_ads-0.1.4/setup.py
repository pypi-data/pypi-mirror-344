from setuptools import setup, find_packages

setup(
    name="llm_ads",
    version="0.1.4",
    description="FastAPI middleware for LLM ad serving integration",
    author="Your Name",
    packages=find_packages(include=["llm_ads", "llm_ads.*"]),
    install_requires=[
        "fastapi",
        "pydantic",
        "starlette",
        "sqlalchemy",
        "asyncpg",
        "python-dotenv",
        "loguru",
	"httpx"
    ],
    python_requires=">=3.8",
) 
