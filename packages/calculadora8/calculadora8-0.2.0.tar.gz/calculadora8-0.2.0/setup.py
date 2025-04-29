from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    descricao_longa = f.read()

setup(
    name='calculadora8',
    version='0.2.0',
    author='Luiz Elias',
    author_email='luizelias8@gmail.com',
    description='Uma calculadora simples para operações básicas',
    long_description=descricao_longa,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
)
