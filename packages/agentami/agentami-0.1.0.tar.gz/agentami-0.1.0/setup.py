from setuptools import setup, find_packages

setup(
    name='agentami',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Amish Gupta',
    author_email='amishgupta@outlook.com',
    description='This project helps create an agent that can handle large number of tools and has persistence',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ami-sh/your-repo',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)