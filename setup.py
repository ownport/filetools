import site

from setuptools import setup

if __name__ == "__main__":
    # enable user site-package directory
    site.ENABLE_USER_SITE = True
    setup()
