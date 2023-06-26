from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pixels-journal-data-processing',
    version='0.1',
    author='Joseph R. Freeston',
    author_email='snorklerjoe@gmail.com',
    description='Processes data exported from Pixels Journal app to find correlation information and more advanced statistics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/snorklerjoe/PixelsJournal-data-processing',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'scipy',
        'rich',
        'click',
        'toml'
    ],
    entry_points={
        'console_scripts': [
            'pixels-journal-data-processing=pixels_journal_data_processing.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)