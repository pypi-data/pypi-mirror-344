from setuptools import setup, find_packages

setup(
    name="drumterm",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "drumterm=drumterm.main:run"
        ]
    },
    package_data={
        "drumterm": ["sounds/*.wav"]
    },
    author="Paul Schmidt",
    description="A terminal drum pad with metronome",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.7"
)
