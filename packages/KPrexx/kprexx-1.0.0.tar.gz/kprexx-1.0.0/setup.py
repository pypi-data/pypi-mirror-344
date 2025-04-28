from setuptools import setup, find_packages

setup(
    name='KPrexx',
    version='1.0.0',
    author='Xscripts Inc.',
    author_email='sunnyplaysyt9@gmail.com',
    description='An advanced keypress handling library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Security',
    ],
    python_requires='>=3.6',
)
