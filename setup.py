from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="6.0.0",  # Sprint 6 version
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["pycryptodome"],
    entry_points={
        "console_scripts": [
            "cryptocore=cryptocore.main:main"
        ]
    }
)