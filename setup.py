# python setup.py bdist_wheel
# twine upload dist/~.whl

from setuptools import setup, find_packages

setup(
    name="creon-api",
    version='1.1',
    url="https://github.com/quantrading/creon-api",
    license="MIT",
    author="Jang Woo Jae",
    author_email="wojae.jang@gmail.com",
    description="daishin creon api",
    install_requires=[
        'pandas',
        'pywin32'
    ],
    packages=find_packages(exclude=['tests', 'docs']),
    python_requires='>=3',
    long_description=open('README.md', encoding='UTF8').read(),
    long_description_content_type="text/markdown",
    package_data={},
    zip_safe=False,
)
