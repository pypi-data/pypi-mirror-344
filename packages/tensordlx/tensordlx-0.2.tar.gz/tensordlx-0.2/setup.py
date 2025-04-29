from setuptools import setup, find_packages

setup(
    name='tensordlx',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'tensorflow',
        'scikit-learn',
        'networkx',
        'tensorflow_hub'
    ],
    author='BabaTunde',
    description='DLcodex',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/my_ml_library',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)