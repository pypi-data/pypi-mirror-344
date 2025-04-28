from setuptools import setup, find_packages

setup(
    name="project-initializer",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "questionary",
        "gitpython",
    ],
    entry_points={
        "console_scripts": [
            "init-project=project_initializer.initilizer:main",
        ],
    },
    url="https://github.com/Soulflys02/web-dev-framework",
    author="Vervloessem Lucas",
    author_email="lucas.vervloessem.atc@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)