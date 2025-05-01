from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'lxml',
    'nltk',
    'pdfminer3',
    'Pillow',
    'setuptools',
    'pdfplumber',
    'requests',
    'numpy',
    'pandas',
    'pyvis',
    'selenium',
    'tinycss',
    'SPARQLWrapper',
    'Tkinterweb',
    'webdriver-manager',
    'scikit-learn',
]

setup(
    name='amilib',
    version='0.5.1a3',
    description='Document and dictionary download, cleaning, management',
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Peter Murray-Rust",
    author_email='petermurrayrust@googlemail.com',
    url='https://github.com/petermr/amilib',
    license='Apache2',
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(include=['amilib', 'amilib.*']),
    package_dir={'amilib': 'amilib'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9, <3.13',
    entry_points={
        'console_scripts': [
            'amilib=amilib.amix:main',
        ],
    },
)

