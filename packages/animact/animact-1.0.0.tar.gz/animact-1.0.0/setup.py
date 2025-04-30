from setuptools import setup, find_packages

setup(
    name='animact',
    version='1.0.0',
    author='Monabbor Hossain',
    author_email='monabborhossainrafi@gmail.com',
    description='Fetch anime action and reaction images easily.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/monabborhossain/animact',
    packages=find_packages(),
    install_requires=[
        'httpx',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)