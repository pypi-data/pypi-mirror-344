from setuptools import setup, find_packages
from pathlib import Path

# Load version from sima_cli/__version__.py
version_path = Path(__file__).parent / "sima_cli" / "__version__.py"
version_ns = {}
exec(version_path.read_text(), version_ns)

setup(
    name="sima-cli",
    version=version_ns["__version__"],
    description="SiMa Developer Portal CLI Tool",
    author="SiMa.ai",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "sima_cli": ["data/*.yaml"],
    },
    install_requires=[
        "click>=8.0",
        "requests>=2.25",
        "tqdm>=4.64"
    ],
    entry_points={
        "console_scripts": [
            "sima-cli=sima_cli.__main__:main"
        ]
    },
    python_requires=">=3.8",
)
