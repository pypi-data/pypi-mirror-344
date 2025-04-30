from setuptools import setup, find_packages

setup(
    name="qrcodex",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pillow>=9.0.0",  # For image handling
    ],
    python_requires=">=3.7",
    author="GamingOP",
    author_email="samratkafle36@gmail.com",
    description="An advanced QR code generator with multiple data type support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GamingOP69/qrcodex",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)