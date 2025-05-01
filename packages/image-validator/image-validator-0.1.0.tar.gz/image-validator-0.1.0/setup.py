from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='image-validator',
    version='0.1.0',
    description='A package to detect fake or low-quality images using OpenCV and Tesseract',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vinayak Gaikwad',
    author_email='gaikwadvinayak1282@gmail.com',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'pytesseract',
        'numpy',
        'Pillow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
