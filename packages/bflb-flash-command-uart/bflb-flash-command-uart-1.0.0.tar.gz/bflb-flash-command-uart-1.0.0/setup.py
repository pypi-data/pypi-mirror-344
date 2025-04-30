#!/usr/bin/env python

from setuptools import setup, find_packages

longdesc = """
## Bouffalolab Flash Command Tool For Uart
====================================

"""

packages = [
    "bflb_flash_command",
    "bflb_flash_command.libs",
    "bflb_flash_command.libs.bl602",
    "bflb_flash_command.libs.bl702",
    "bflb_flash_command.libs.bl702l",
    "bflb_flash_command.libs.bl808",
    "bflb_flash_command.libs.bl616",
    "bflb_flash_command.libs.bl616l",
    "bflb_flash_command.libs.bl616d",
    "bflb_flash_command.libs.bl628",
]

entry_points = {"console_scripts": ["bflb-flash-command-uart = bflb_flash_command.__main__:run_main"]}

setup(
    name="bflb-flash-command-uart",
    version="1.0.0",
    author="bouffalolab",
    author_email="jxtan@bouffalolab.com",
    description="Bouffalolab Flash Command Tool",
    long_description=longdesc,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://pypi.org/project/bflb-flash-command-uart/",
    packages=packages,  # 包的代码主目录
    # package_data=package_data,
    include_package_data=True,
    entry_points=entry_points,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Unix",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "toml==0.10.0",
        "configobj==5.0.9",
        "cryptography==37.0.4",
        "pyserial==3.5",
        "pylink-square==0.5.0",
        "pycklink>=0.1.1",
        "telnetlib-313-and-up; python_version>'3.12'"
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
