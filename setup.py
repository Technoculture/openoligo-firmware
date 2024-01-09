from setuptools import setup, find_packages

setup(
    name="OpenOligo",
    version="0.1.8",
    description="An open-source platform for programmatically interacting with and managing Nucleic acid sequences synthesis processes.",
    license="Apache-2.0",
    author="Satyam Tiwary",
    author_email="satyam@technoculture.io",
    packages=find_packages(),
    install_requires=[
        "rich>=13.4.2",
        "python-dotenv>=1.0.0",
        "tqdm>=4.65.0",
        "fastapi>=0.98.0",
        "pdocs>=1.2.0",
        "uvicorn>=0.22.0",
        "aerich>=0.7.1",
        "types-tqdm>=4.65.0.1",
        "tortoise-orm>=0.18.1",
        "pydantic>=1.8.2",
        "httpx>=0.24.1",
        "sh>=2.0.4",
        "anyio>=3.7.0",
        "types-requests>=2.31.0.1",
    ],
    extras_require={
        "rpi": ["RPi.GPIO>=0.7.1"],
        "bb": ["Adafruit_BBIO>=1.2.0"],
    },
    entry_points={
        'console_scripts': [
            'oligo-server=openoligo.scripts.server:main',
            'oligo-runner=openoligo.scripts.runner:main',
            'oligo=openoligo.scripts.orchestrator:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires='>=3.9',
)
