from setuptools import setup

setup(
    name = 'firmware',
    packages = ['firmware'],
    include_package_data = True,
    install_requires = [
        'flask',
    ],
)
