from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AvidaScripts",
    version="0.4.1",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=requirements,
    author="Matthew Andres Moreno",
    author_email="morenoma@umich.edu",
    description="Repack of Luis Zaman's AvidaScripts as an installable package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmore500/AvidaScripts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
