from distutils.core import setup, Extension


with open('README.txt') as file:
    long_description = file.read()

setup(
    name="decimalfp",
    version="0.9.12",
    author="Michael Amrhein",
    author_email="michael@adrhinum.de",
    url="https://pypi.python.org/pypi/decimalfp",
    description="Decimal fixed-point arithmetic",
    long_description=long_description,
    py_modules=['decimalfp', '_pydecimalfp'],
    ext_modules=[Extension('_cdecimalfp', ['_cdecimalfp.c'])],
    license='BSD',
    keywords='fixed-point decimal number datatype',
    platforms='all',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
