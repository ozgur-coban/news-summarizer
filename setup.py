from setuptools import setup
import subprocess

# Install model/data downloads after pip install
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
subprocess.run(["python", "-m", "nltk.downloader", "stopwords", "wordnet", "omw-1.4"])

setup(
    name="bart-ensemble-summarizer",
    version="0.1",
    install_requires=open("requirements.txt").read().splitlines(),
)
