from setuptools import setup, find_packages

setup(
    name='interfaceMl',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'numpy',
        'aniso8601',
        'click',
        'Flask-RESTful',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'nose',
        'npm',
        'numpy',
        'optional-django',
        'python-dateutil',
        'pytz',
        'scikit-learn',
        'scipy',
        'six',
        'Werkzeug',
        'numpydoc',
    ],
)
