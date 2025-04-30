from setuptools import setup, find_packages

setup(
    name='algonix',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-learn'
    ],
    author='Bhushan Zade',
    author_email='bhushanzade02@gmail.com',
    description='Algonix: A simple machine learning library with custom models, optimizers, and metrics.',
    url='https://github.com/bhushanzade02/MACHINE-LEARNING',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    python_requires='>=3.6',
)
