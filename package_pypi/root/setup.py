# setup.py

from pathlib import Path
from setuptools import setup, find_packages,find_namespace_packages

this_directory = Path(__file__).parent

setup(
    name="simu_docker_rpi",
    version="0.1.8",
    author="Unlam",
    description="Bibloteca para usar el emulador de Raspberry Pi dentro de Docker",
    long_description=open(this_directory/"README.md").read(),
    long_description_content_type="text/markdown",
    #packages=find_packages(),
    packages=find_namespace_packages(include=["simu_docker_rpi", "simu_docker_rpi.*"]),
    include_package_data=True,  # Esto indica que use MANIFEST.in
    install_requires=[
        "cffi",
        "colorzero",
        "paho-mqtt<2.0.0", 
        "pigpio",
        "pillow",
        "pycparser",
        "setuptools",
        "sounddevice"
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
