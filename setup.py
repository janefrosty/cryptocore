from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="7.0.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["pycryptodome"],
    entry_points={
        "console_scripts": [
            "cryptocore=cryptocore.main:main"
        ]
    }
)