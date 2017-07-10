from setuptools import setup, find_packages

setup(
    name='interfaceMl',
    version='0.0.0a1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-RESTful',
        'scikit-learn',
        'numpydoc',
        'scikit-plot',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-flask'
    ]
)
