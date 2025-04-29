from setuptools import setup, find_packages

setup(
    name="id3classifier_mystyle",  # Name of the package
    version="0.1",  # Version number
    packages=find_packages(),  # Automatically find packages
    install_requires=[  # External dependencies
        'pandas',
        'numpy',
        'graphviz',
    ],
    description="ID3 Classifier implementation",  # Short description
    long_description=open('README.md').read(),  # Read from the README file
    long_description_content_type='text/markdown',  # Markdown format for long description
    author="Your Name",  # Your name
    author_email="your_email@example.com",  # Your email
    url="https://github.com/yourusername/id3_classifier",  # Optional: Add URL to the package
    classifiers=[  # Optional: Add classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
