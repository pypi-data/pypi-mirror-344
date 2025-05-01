from setuptools import setup

setup(
    name="trustlint",
    version="1.0.0",
    packages=["trustlint"],
    package_dir={"trustlint": "."},
    package_data={"trustlint": ["index.ts"]},
    include_package_data=True,
    python_requires=">=3.7",
)
