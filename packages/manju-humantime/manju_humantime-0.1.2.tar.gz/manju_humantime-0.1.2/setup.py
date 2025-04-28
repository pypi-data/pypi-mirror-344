from setuptools import setup, find_packages

setup(
    name="manju_humantime",
    version="0.1.4",
    packages=find_packages(),
    description="A simple utility to humanize time differences",
    author="Manjunathgouda MH",
    author_email="manjumh021@gmail.com",
    url="https://github.com/manjumh021/manju-humantime",  # (optional, if you have GitHub repo)
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
