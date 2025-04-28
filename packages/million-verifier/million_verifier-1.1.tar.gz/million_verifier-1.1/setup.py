import sys

from setuptools import setup, find_packages

version_range_max = max(sys.version_info[1], 10) + 1

setup(
    name='million_verifier',
    version='1.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license="Apache 2.0 License",
    install_requires=["requests"],
    include_package_data=True,
    long_description=open('README.rst', "r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Alex',
    classifiers=[
                    "Development Status :: 5 - Production/Stable",
                    "Intended Audience :: Developers",
                    "Intended Audience :: Education",
                    "Intended Audience :: Science/Research",
                    "License :: OSI Approved :: Apache Software License",
                    "Operating System :: OS Independent",
                    "Topic :: Scientific/Engineering :: Artificial Intelligence",
                    "Programming Language :: Python :: 3",
                ] + [f"Programming Language :: Python :: 3.{i}" for i in range(8, version_range_max)],
    python_requires='>=3.8'

)