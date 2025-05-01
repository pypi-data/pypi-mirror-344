from setuptools import setup, find_packages

setup(
    name='animact',
    version='1.1.0',
    author='Monabbor Hossain',
    author_email='monabborhossain@gmail.com',
    description='Anime-themed action and reaction image API wrapper for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/monabborhossain/animact',
    project_urls={
        'Documentation': 'https://github.com/monabborhossain/animact#readme',
        'Source': 'https://github.com/monabborhossain/animact.git',
        'Issues': 'https://github.com/monabborhossain/animact/issues',
    },
    packages=find_packages(),
    install_requires=[
        'httpx>=0.24.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['anime', 'reaction', 'image', 'api', 'async'],
    python_requires='>=3.7',
)