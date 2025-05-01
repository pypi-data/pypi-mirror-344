import setuptools
import distutils.core

setuptools.setup(
    name='env-subset',
    version="1.1.0",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='Run a command with the subset of the current environment. env swiss army knife',
    license='BSD',
    keywords='cli,environment',
    url='https://github.com/talwrii/env-subset',
    packages=["env_subset"],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['env-subset=env_subset.main:main']
    }
)
