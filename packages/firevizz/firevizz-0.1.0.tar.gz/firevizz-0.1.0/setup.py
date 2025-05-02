from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="firevizz",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "folium>=0.12.0",
        "scikit-learn>=1.0.0",
        "joblib>=1.0.0"
    ],
    author="Ripunjay Singh",
    author_email="ripunjaysingh2104114@dei.ac.in",  # Replace with your email
    description="A Python library for visualizing and analyzing fire detection data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RipunjayS109/firevizz",  # Replace with your GitHub URL
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
    keywords="fire detection, visualization, mapping, sensor data",
) 