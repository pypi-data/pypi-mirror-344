from setuptools import setup, find_packages

with open('README.md', 'r') as f:
  description = f.read()

setup(
    name="ez-route",
    version="0.1.1",
    description="A lightweight routing system for GUI applications (PyQt, Tkinter, etc.)",
    author="Myo Thant",
    author_email="myothant.thedev@gmail.com",
    url="https://github.com/MyothantTheDev/ez_route",
    packages = find_packages(where="src"),
    package_dir = {"": "src"},
    install_requires = [],
    extras_require = {
        "qt": ["PyQt6"],     # if users want Qt support
        "tk": ["tk"],        # Tkinter is standard
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    long_description=description,
    long_description_content_type='text/markdown'
)
