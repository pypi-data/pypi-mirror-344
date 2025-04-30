from setuptools import setup

VERSION = "0.0.1"
SHORT_DESCRIPTION = "Twitter X-Client-Transaction-Id generator written in python."


setup(
    name="x-client-transaction-id",
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description="""This is a copy of XClientTransaction package. Check more details on [XClientTransaction](https://pypi.python.org/pypi/XClientTransaction).""",
    long_description_content_type="text/markdown",
    author="Sarabjit Dhiman",
    author_email="hello@sarabjitdhiman.com",
    license="MIT",
    url="https://pypi.python.org/pypi/XClientTransaction",
    keywords=["XClientTransaction", "twitter transaction id", "client transaction id twitter",
              "tid generator", "x client transaction id generator",
              "xid twitter", "tweeterpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
    ],
    install_requires=['XClientTransaction'],
    python_requires=">=3"
)
