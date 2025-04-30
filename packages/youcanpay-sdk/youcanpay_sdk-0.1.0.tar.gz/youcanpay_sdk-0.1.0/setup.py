from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as f:
    license_text = f.read()

setup(
    name="youcanpay-sdk",
    version="0.1.0",
    author="Yassir AIT EL AIZZI",
    author_email="yassir.aitelaizzi@gmail.com",
    description="SDK for integrating YouCan Pay API with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yassir-aea/youcanpay",
    project_urls={
        "Homepage": "https://github.com/yassir-aea/youcanpay",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
    license="MIT",
    include_package_data=True,
) 