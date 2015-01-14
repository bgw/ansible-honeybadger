from setuptools import setup

setup(name="ansible-honeybadger",
      install_requires=["ansible>=1.8.2,<1.9",
                        "inquirer>=2.1.2,<2.2",
                        "pyyaml>=3.11,<4.0"])
