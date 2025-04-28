from setuptools import setup, find_packages

VERSION = '0.4' 
DESCRIPTION = 'Examining SHared Alleles? Yes!'
LONG_DESCRIPTION = 'A package to look at similarity between two genetic datasets. Useful for finding duplicate tissue donors betwen studies.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="EShAY", 
        version=VERSION,
        author="Dr Gabe O'Reilly",
        author_email="<g.oreilly@garvan.org,au>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['python', 'test', 'Genetics', 'Diversity'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
