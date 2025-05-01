from setuptools import setup, find_packages

setup(
    name="PyWaves-CE",
    version="1.0.5",
    description="Object-oriented library for the Waves blockchain platform",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="PyWaves Developers",
    author_email="dev@pywaves.org",
    url="https://github.com/PyWaves-CE/PyWaves-CE",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "base58==0.2.5",
        "python-axolotl-curve25519",
        "requests",
        "google-api-python-client",
        "protobuf==3.19.6"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="waves blockchain analytics",
    python_requires=">=3.6",
)
