from setuptools import setup, find_packages

setup(
    name="AvidaScripts",
    version="0.0",
    packages=["AvidaScripts"],
    package_dir={'': '.'},
    author="Matthew Andres Moreno",
    author_email="morenoma@umich.edu",
    description="Repack of Luis Zaman's AvidaScripts as an installable package.",
    long_description=open('README').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmore500/AvidaScripts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
