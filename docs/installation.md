# Installation

At the command line:

    pip install kosu

Or, if you use Conda environments:

    conda create -n kosu python=3.9
    conda activate kosu
    pip install kosu

To install with the option of uploading course material to an Amazon AWS S3 bucket, [install and set up Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) yourself, or use the `aws` option with `pip` like so:

    pip install kosu[aws]

**Please note that `kosu` is a command line utility, and is not generally used from within Python.**

For developers, there are also options for installing `tests`, `docs` and `dev` dependencies.

If you want to help develop `kosu`, please read [Development](development.md).
