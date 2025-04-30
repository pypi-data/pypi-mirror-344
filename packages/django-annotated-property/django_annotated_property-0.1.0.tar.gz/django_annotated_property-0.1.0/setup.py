from setuptools import setup, find_packages

setup(
    name='django-annotated-property',
    version='0.1.0',
    description='Decorator for Django model properties that checks if an annotation exists on the instance.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Milan Slesarik',
    author_email='milslesarik@gmail.com',
    url='https://github.com/milano-slesarik/django-annotated-property',
    packages=find_packages(),
    install_requires=[
        'Django>=2.2',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
