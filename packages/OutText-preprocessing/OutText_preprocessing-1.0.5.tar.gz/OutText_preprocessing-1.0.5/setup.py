from setuptools import setup, find_packages
import os

# Read README content safely
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.rst"), encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='OutText_preprocessing',
    version='1.0.5',
    description='✨ A powerful Python package for outlier removal and text preprocessing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anurag Raj',
    author_email='anuragraj4483@gmail.com',
    url="https://github.com/Anurag-raj03/OutText_preprocessing_library",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "scikit-learn",
        "nltk",
        "emoji",
        "autocorrect",
        "pytest",
    ],
    python_requires='>=3.6',
)
