import setuptools

setuptools.setup(
    name="vmx-aps",
    version="2.3.0",
    author="Verimatrix Inc.",
    author_email="blackhole@verimatrix.com",
    description="APS command line wrapper",
    long_description="APS command line wrapper",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-dateutil",
        "requests",
        "pyaxmlparser",
        "backoff",
        "coloredlogs"
    ],
    entry_points={
        "console_scripts": [
            "vmx-aps=apsapi.aps:main",
        ],
    },
)
