from setuptools import setup, find_packages

setup(
    name="OpenOligo",
    version="0.1.3",
    author="Satyam Tiwary",
    author_email="satyam@technoculture.io",
    description="An open-source platform for programmatically interacting with and managing Nucleic acid sequences synthesis processes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "rich>=13.4.2",
        "python-dotenv>=1.0.0",
        "biopython>=1.81",
        "tqdm>=4.65.0",
        "fastapi>=0.98.0",
        "pdoc3>=0.10.0",
        "pdocs>=1.2.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.2",
            "pytest-cov>=4.1.0",
            "flake8>=3.9.2",
            "black>=23.3.0",
            "pylint>=2.17.4",
            "mypy>=1.3.0",
            "isort>=5.12.0",
            "coverage-badge>=1.1.0",
            "jupyter>=1.0.0",
            "jupyterlab>=4.0.2",
            # "ansible>=8.1.0",
        ],
        "rpi": ["RPi.GPIO"],
        "bb": ["Adafruit_BBIO"]
    },
    python_requires=">=3.9",
    classifiers=[ "DNA", "synthesis", "genetics", "open-source" ],
    entry_points={
        "console_scripts": [
            "oligo-server=app.server:main",
            "oligo-synth=examples.dna_synthesis:main",
        ],
    },
)

