from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nlpkwords',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'nltk>=3.6.0',
        'textblob>=0.15.3',
        'scikit-learn>=0.24.0',
        'numpy>=1.20.0',
    ],
    author='Rish Dias',
    author_email='rishrdias672004@gmail.com',
    description='A package containing AI/ML codes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nOTpROGRAMMERr/nlpkwords',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='nlp, machine learning, artificial intelligence, education',
    python_requires='>=3.6',
    include_package_data=True,
)
