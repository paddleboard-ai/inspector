from setuptools import setup, find_packages

setup(
    name='data-inspector',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'pyarrow',
    ],
    entry_points='''
        [console_scripts]
        inspector=inspector:inspect_file
    ''',
)