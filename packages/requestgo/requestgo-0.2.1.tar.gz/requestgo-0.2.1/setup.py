
from setuptools import setup, Extension

fast_response = Extension('fast_response', sources=['fast_response.c'])

setup(
    name="requestgo",
    version="0.2.1",
    description="A fast, stealthy, no-dependency HTTP request library",
    author="Cansila",
    packages=["requestgo"],
    ext_modules=[fast_response],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
