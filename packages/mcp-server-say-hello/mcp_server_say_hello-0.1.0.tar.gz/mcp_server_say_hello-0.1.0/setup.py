from setuptools import setup, find_packages

setup(
    name="mcp_server_say_hello",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "packaging>=24.2"
    ],
    entry_points={
        "console_scripts": [
            "mcp-say-hello = mcp_server_say_hello.__main__:main"
        ]
    },
    python_requires=">=3.9",
)