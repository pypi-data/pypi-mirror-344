from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sortepack",
    version="0.0.1",
    author="Andi",
    author_email="andissaura@gmail.com",
    description="Pacote para sortear números e itens aleatórios.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andissaura/simple-package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)