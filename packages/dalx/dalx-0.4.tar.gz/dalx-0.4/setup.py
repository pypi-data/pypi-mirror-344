from setuptools import setup, find_packages, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dalx",
    version="0.4", # Update the version before publishing to pypi
    author="Ashborn",
    description="No description provided",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    license_files=("LICENSE.txt",),
    package_dir={"ashborn": "src/ashborn"},
    package_data = {'ashborn':['data/**']},
    include_package_data=True,
    packages=find_namespace_packages(where='src'),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    zip_safe=False,
)
