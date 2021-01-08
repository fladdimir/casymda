"""setuptools setup"""

from setuptools import find_packages, setup

VERSION = "0.2.25"

try:
    with open("readme.md") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""


setup(
    name="casymda",
    url="https://github.com/fladdimir/casymda",
    author="FFC",
    author_email="fladdi.mir@gmx.de",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "casymda.visualization.state_icons": ["*.png"],
        "casymda.visualization.web_server": ["*.html", "*.js"],
    },
    version=VERSION,
    install_requires=[
        "simpy",
        "xmltodict",
        "Pillow",
        "flask",
        "flask-cors",
        "black==19.3b0",
        "numpy",
        "networkx",
    ],
    zip_safe=False,
    license="MIT",
    description="A simple DES modeling and simulation environment"
    + " based on simpy, camunda modeler, and tkinter / pixi.js;",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
