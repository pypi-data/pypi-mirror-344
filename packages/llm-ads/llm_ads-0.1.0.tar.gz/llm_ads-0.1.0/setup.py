from setuptools import setup, find_packages

setup(
    name='llm_ads',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy>=2.0.0',
        'asyncpg>=0.27.0',
        'pydantic>=2.0.0',
        'fastapi>=0.100.0',
        'starlette>=0.27.0',
        'loguru>=0.7.0',
        'python-dotenv>=1.0.0',
        'httpx>=0.24.0',
    ],
    description='Ad-serving middleware for LLMs',
    author='Ravi Shah',
)
