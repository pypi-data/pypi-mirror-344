[![Github Actions](https://github.com/GSA/ckanext-datagovcatalog/actions/workflows/test.yml/badge.svg)](https://github.com/GSA/ckanext-datagovcatalog/actions)
[![PyPI version](https://badge.fury.io/py/ckanext-datagovcatalog.svg)](https://badge.fury.io/py/ckanext-datagovcatalog)

# ckanext-datagovcatalog

[comment]: <> (Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!)

# Data.gov  

[Data.gov](http://data.gov) is an open data website created by the [U.S. General Services Administration](https://github.com/GSA/) that is based on two robust open source projects: [CKAN](http://ckan.org) and [WordPress](http://wordpress.org). The data catalog at [catalog.data.gov](catalog.data.gov) is powered by CKAN, while the content seen at [Data.gov](Data.gov) is powered by WordPress.  
        
**For all code, bugs, and feature requests related to Data.gov, see the project wide Data.gov [issue tracker](https://github.com/GSA/data.gov/issues).** 

Currently this repository is only used for source version control on the code for the CKAN extension for datagovcatalog features, but you can see all of the Data.gov relevant repos listed in the [GSA Data.gov README file](https://github.com/GSA/data.gov/blob/master/README.md). 

# Requirements

For example, you might want to mention here which versions of CKAN this
extension works with.


Package                                                                | Notes
---------------------------------------------------------------------- | -------------
[ckanext-harvest](https://github.com/ckan/ckanext-harvest/)            | This currently has two different version for py2 and py3 until [this PR](https://github.com/ckan/ckanext-harvest/pull/450) is merged upstream
[ckanext-envvars](https://github.com/okfn/ckanext-envvars)             | This is necessary based on how the testing environment is set up.


# Installation

[comment]: <> (Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.)

CKAN version | Compatibility
------------ | -------------
<=2.8        | no
2.9          | 0.0.5 (last supported)
2.10         | >=0.1.0

To install ckanext-datagovcatalog:

1. Activate your CKAN virtual environment, for example::

     `. /usr/lib/ckan/default/bin/activate`

2. Install the ckanext-datagovcatalog Python package into your virtual environment::

     `pip install ckanext-datagovcatalog`

3. Add ``datagovcatalog`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     `sudo service apache2 reload`


# Config Settings

[comment]: <> (Document any optional config settings here. For example::

    # Add tracking info on each package for the dataset lists
    # (optional, default: true).
    ckanext.datagovcatalog.add_packages_tracking_info = true)


# Development Installation

To install ckanext-datagovcatalog for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/GSA/ckanext-datagovcatalog.git
    cd ckanext-datagovcatalog
    python setup.py develop
    pip install -r requirements.txt
    pip install -r dev-requirements.txt

**Note: use the py2-equivalents of the requirement files if running on python 2.

# Running the Tests

## Tests

## Using the Docker Dev Environment

### Build Environment

To start environment, run:
```make build```
```make up```

CKAN will start at localhost:5000

To shut down environment, run:

```make clean```

To docker exec into the CKAN image, run:

```docker-compose exec app /bin/bash```

### Testing

They follow the guidelines for [testing CKAN
extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the extension tests,

    $ make test

Lint the code.

    $ make lint
    
### Matrix builds

The existing development environment assumes a minimal catalog.data.gov test setup. This makes
it difficult to develop and test against dependencies with other extensions.

In order to support multiple versions of CKAN, or even upgrade to new versions
of CKAN, we support development and testing through the `CKAN_VERSION`
environment variable.

    $ make CKAN_VERSION=2.10 test

# Registering ckanext-datagovcatalog on PyPI

ckanext-datagovcatalog should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-datagovcatalog. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


# Releasing a New Version of ckanext-datagovcatalog

ckanext-datagovcatalog is availabe on PyPI as https://pypi.python.org/pypi/ckanext-datagovcatalog.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
