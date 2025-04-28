from setuptools import setup, find_packages

with open("desc.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="fpowerkit",
    version="0.3.0",
    author="fmy_xfk",
    packages=find_packages(),
    description="A Distflow PDN solver based on Gurobi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["feasytools>=0.0.21", "numpy>=1.19.0"],
)