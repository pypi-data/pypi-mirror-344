from setuptools import setup, find_packages

setup(
    name='francalculator',  # Nome do seu pacote
    version='0.3',
    description='Biblioteca para cálculos matemáticos e engenharia',  # Descrição do seu pacote
    author='Lukydnomo',  # Seu nome
    packages=find_packages(),  # Encontra automaticamente os pacotes
    install_requires=[  # Dependências, se houver
        "requests", "pathlib", "re", "math", "sys", "random", "datetime", "ast", "operator", "logging", "traceback", "colorama", "shutil"
    ],
    classifiers=[  # Classificadores para ajudar na busca
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versão mínima do Python
)
