from setuptools import setup, find_packages

setup(
    name='id3classifier-mystyle',
    version='0.2',
    packages=find_packages(),  # <-- this automatically finds the id3_classifier package
    install_requires=[
        'pandas',
        'numpy',
        'graphviz',
    ],
    author='Srinu Vakada',
    author_email='your.email@example.com',
    description='An ID3 Decision Tree Classifier',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/id3classifier-mystyle/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
