from setuptools import setup, find_namespace_packages

setup(
    url="https://q-chem.com",
    author_email="support@q-chem.com",
    description="Utility for setting up Q-Cloud administrators",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(where="src"), 
    package_dir={'qcloud_setup': 'src/qcloud_setup'},
    package_data={'qcloud_setup': ['*.yaml']},
    include_package_data=True,
    license_files=["LICENSE.txt"],

    install_requires=[
        "demjson3>=3.0.6",
        "paramiko>=3.4.0",
        "pick>=2.2.0",
        "PyYAML==5.3.1",
        "pyopenssl>=22.1.0",
        "Requests>=2.31.0",
        "aws-parallelcluster==3.6.0"
    ],
    scripts=['src/qcloud_setup/qcloud_admin.py'],
)
