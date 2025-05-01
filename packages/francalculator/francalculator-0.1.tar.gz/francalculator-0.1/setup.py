from setuptools import setup, find_packages

setup(
    name='francalculator',  # Nome do seu pacote
    version='0.1',  # Versão inicial
    description='Biblioteca para cálculos matemáticos e engenharia',  # Descrição do seu pacote
    author='Lukydnomo',  # Seu nome
    packages=find_packages(),  # Encontra automaticamente os pacotes
    install_requires=[  # Dependências, se houver
        # 'requests',  # Exemplo de dependência
    ],
    classifiers=[  # Classificadores para ajudar na busca
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versão mínima do Python
)
