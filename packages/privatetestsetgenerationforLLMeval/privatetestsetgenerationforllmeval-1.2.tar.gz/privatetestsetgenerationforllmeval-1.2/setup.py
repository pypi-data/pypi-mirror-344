from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='privatetestsetgenerationforLLMeval',
    version='1.2',
    author='Ilias',
    author_email='ilias.driouich@amadeus.com',
    description='A package for generating evaluation set for LLM-based chatbots in a diverse and private manner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AmadeusITGroup/privatetestsetgenerationforLLMeval',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas>=1.1.0',
        'numpy>=1.19.0',
    ],
    tests_require=[
        'pytest>=6.0.0',
    ],
    entry_points={
        'console_scripts': [
            'privatetestsetgeneration=run.run:main',
    ],
    },
    python_requires='>=3.6',
)
