import setuptools

setuptools.setup(
    name="octoauth",
    description="",
    version="0.0.1-beta",
    packages=setuptools.find_packages(),
    install_requires=["aiofiles", "fastapi", "pydantic", "sqlalchemy", "uvicorn"],
    extras_require={"dev": ["black", "isort", "pylint", "pytest"]},
    entry_points={"console_scripts": ["octo=octoauth.__main__:main"]},
)
