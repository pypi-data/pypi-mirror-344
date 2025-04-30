from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ml_derivatives",
    version="0.0.2",
    keywords="Signal processing, data science, filtering, derivation, de-noising",
    description="A python module for computing high derivatives of noisy time-series",
    author="Mazen Alamir",
    author_email="mazen.alamir@grenoble-inp.fr",
    long_description=long_description,
    long_description_content_type="text/markdown",  # or "text/x-rst" for .rst files
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "joblib==1.4.2",
        "numpy==2.2.5",
        "pandas==2.2.3",
        "python-dateutil==2.9.0.post0",
        "pytz==2025.2",
        "scikit-learn==1.6.1",
        "scipy==1.15.2",
        "six==1.17.0",
        "threadpoolctl==3.6.0",
        "tqdm==4.67.1",
        "tzdata==2025.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)