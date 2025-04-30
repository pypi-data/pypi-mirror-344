import setuptools

from skactiveml import __version__


def readme():
    with open("README.rst", "r") as f:
        return f.read()


def requirements():
    with open("requirements.txt", "r") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


setuptools.setup(
    name="scikit-activeml",
    version=__version__,
    description="Our package scikit-activeml is a Python library "
    "for active learning on top of SciPy and "
    "scikit-learn.",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "active learning",
        "machine learning",
        "semi-supervised learning",
        "data mining",
        "pattern recognition",
        "artificial intelligence",
    ],
    url="https://github.com/scikit-activeml/scikit-activeml",
    author="Marek Herde",
    python_requires=">=3.9",
    author_email="marek.herde@uni-kassel.de",
    license="BSD 3-Clause License",
    license_file='LICENSE',
    packages=setuptools.find_packages(),
    install_requires=requirements(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
    zip_safe=False,
)
