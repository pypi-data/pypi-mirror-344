from setuptools import setup, find_packages
import os

setup(
    name="reframe-cli",
    version="1.1.1",
    description="ReFrame-CLI is a Python-based command-line tool to streamline your video and image manipulation tasks. Ideal for preparing image datasets for training machine learning models, including generative AI and diffusion models. Can handle videos of any length.",
    long_description=open("readme.md").read() if os.path.exists("readme.md") else "",
    long_description_content_type="text/markdown",
    author="Gour4v",
    author_email="chatgai.note@gmail.com",
    license="MIT",
    packages=find_packages(include=["ReFrame", "ReFrame.*"]),
    install_requires=[
        "opencv-python",
        "pillow",
        "imageio",
        "pillow-heif",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "reframe=ReFrame.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    project_urls={
        "GitHub": "https://github.com/ForgeL4bs/ReFrame",
        "Documentation": "https://github.com/ForgeL4bs/ReFrame#readme",
        "Issue Tracker": "https://github.com/ForgeL4bs/ReFrame/issues",
    },
)