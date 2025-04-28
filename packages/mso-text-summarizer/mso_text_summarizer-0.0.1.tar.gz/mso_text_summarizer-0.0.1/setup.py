from setuptools import setup, find_packages

setup(
    name='mso_text_summarizer',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "nltk",
        "numpy",
        "datasets",
        "sumy"
    ],
    author='Ivasiuk Mykhailo, Sofiia Popeniuk, Ostap Pavlyshyn',
    description='Text summarization project SVD',
    python_requires='>=3.7',
)
