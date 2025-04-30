import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="groupify",
    version="0.1.8",
    author="René Alexander Ask",
    author_email="rene.ask@icloud.com",
    description="Automatically generates random groups from a class list.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reneaas/groupify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "seaborn",
    ],
    python_requires=">=3.7",
)
