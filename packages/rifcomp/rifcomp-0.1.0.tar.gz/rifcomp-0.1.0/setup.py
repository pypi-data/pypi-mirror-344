from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:  # Укажите кодировку
    long_description = fh.read()

setup(
    name="rifcomp",
    version="0.1.0",  # Укажите версию (обязательно) - лучше SemVer
    packages=find_packages(),  # Находит пакеты в вашей библиотеке (важно для пакетов)
    install_requires=["requests", "Pillow"],
    author="Rifleks",
    author_email="r.burdakov2022@yandex.ru",  # Добавьте email
    description="Конвертер валют, единиц и файлов",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rifleks/rifcomp",  # Добавьте ссылку на репозиторий (если есть)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Исправлено написание
        "Operating System :: OS Independent",  # Добавьте классификатор
    ],
    python_requires='>=3.6',  # Укажите минимальную версию Python
)