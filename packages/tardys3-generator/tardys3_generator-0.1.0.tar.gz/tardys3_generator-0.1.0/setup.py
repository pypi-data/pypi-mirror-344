from setuptools import setup, find_packages

setup(
    name="tardys3-generator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jsonschema>=4.0.0",
    ],
    entry_points={
        'console_scripts': [
            'tardys3-generator = tardys3_generator.gui:main',
        ],
    },
    package_data={
        'tardys3_generator': ['tardys3_schema.json'],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A TARDyS3 reservation file generator and validator for CBRS P-DPAs.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/tardys3-generator",  # (if you have GitHub repo)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
