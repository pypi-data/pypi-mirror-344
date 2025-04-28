import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="NexusPythonWrapper",
    version="0.0.10",
    description="REST API Wrapper library for NEXUS Integrity Centre",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matthew Irvine",
    author_email="mattew.irvine44@gmail.com",
    url="https://github.com/matthewirvine4/NexusPythonWrapper",
    license="MIT",
    project_urls={
        "Source": "https://github.com/matthewirvine4/NexusPythonWrapper",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
    python_requires=">=3.11",
    install_requires=[
        "requests",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={"console_scripts": ["NexusPythonWrapper = NexusPythonWrapper:main"]},
)