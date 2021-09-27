import setuptools

setuptools.setup(
    name="octoauth",
    description="",
    version="0.0.1-beta",
    packages=setuptools.find_packages(),
    install_requires=["sqlalchemy"],
    extras_require={"dev": ["black", "isort", "pytest"]},
)
