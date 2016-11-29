from setuptools import setup

setup(name="ansible-honeybadger",
      install_requires=["ansible>=2.2,<2.3",
                        "inquirer>=2.1.11,<2.2",
                        "pyyaml>=3.12,<4.0"])
