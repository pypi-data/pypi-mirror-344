from setuptools import setup, find_packages

setup(
    name="vidot-viz",  # PyPI requires hyphen-separated names
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "vidot_viz=vidot_viz.__main__:main",  # Changed from xdot to vidot_viz
        ]
    },
    install_requires=[
        "pycairo>=1.23.0",
        "PyGObject>=3.42.0"
    ],
    include_package_data=True,
    package_data={
        "vidot_viz": ["ui/*.glade"]  # Include GTK UI files
    },
    python_requires=">=3.6",
    description="Interactive Verilog visualization tool with GTK interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aliqyan",
    author_email="your@email.com",
    url="https://github.com/aliqyan-21/vidot",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
