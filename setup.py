from setuptools import setup, find_packages
from dumpmyscreen.version import __version__

setup(
    name="dumpmyscreen",
    version=__version__,
    description="A lightweight, simple and effective screenshot tool, that enables custom commands to be copied to the clipboard.",
    author="Sebastian Westberg",
    author_email="sebastian@westberg.io",
    url="https://github.com/Hibbins/dumpmyscreen",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dumpmyscreen=dumpmyscreen.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications",
        "Framework :: PyQt",
        "Topic :: Utilities :: Graphics :: Capture",
    ],
    python_requires=">=3.6",
)
