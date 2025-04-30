from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="thonny-data_visualization-Collins_v1.0",
    version="2.0.0",
    description="A Thonny plug-in to visualize your data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sedemsenaya/",
    author=["Collins Sedem"],
    author_email=["Collinssed1@gmail.com"],
    license="UCLouvain",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    keywords="Thonny, data visualization",
    packages=['thonnycontrib.data_visualization', 'thonnycontrib.data_visualization.Graphical'],
    python_requires=">=3.7",
    install_requires=["thonny>=4.1.4", "networkx"]
)