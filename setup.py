from setuptools import setup, find_packages

setup(
    name="acit4420-final",  # Replace with your project name
    version="1.0.0",
    description="Final assignment for ACIT4420, including Thoughtful Planner and File Organizer",
    author="Ahsan Habib Sonar",
    url="https://github.com/ahsanhabibsonar/acit4420-final",  # Replace with your GitHub URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "networkx",
        "matplotlib",
        "pytest",
        "pytest-cov",
        "geopy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

