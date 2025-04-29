from setuptools import setup, find_packages

setup(
    name="transformative_harmonization",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
    ],
    author="Zayn",
    description="A Python library for Transformative Harmonization, a novel similarity metric",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zayn/transformative_harmonization",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
)