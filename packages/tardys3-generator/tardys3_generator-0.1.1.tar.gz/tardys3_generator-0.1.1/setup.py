from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tardys3-generator",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jsonschema>=4.0.0",
        "tkcalendar>=1.6.1",
    ],
    entry_points={
        'console_scripts': [
            'tardys3-generator = tardys3_generator.gui:main',
        ],
    },
    package_data={
        'tardys3_generator': ['tardys3_schema.json'],
    },
    author="Masheenist",
    author_email="syll7976@colorado.edu",
    description="A TARDyS3 reservation file generator and validator for CBRS P-DPAs.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/tardys3-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
