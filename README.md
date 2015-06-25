Goodreads client |build-status|
===============================

A simple client wrapping parts of the Goodreads API in Python.


App authorization
-----------------
After setting up the developer credentials and storing them as
environment variables CLIENT_ID and CLIENT_SECRET,
authorizing the app (needed to be done once) is as simple as:

.. code-block:: pycon

    >>> from goodreads import GoodreadsClient
    >>> GoodreadsClient.authorize_access()


Accessing the API
-----------------
Once the above is run, this is pretty simple.

.. code-block:: pycon

    >>> from goodreads import GoodreadsClient
    >>> client = GoodreadsClient()

### Information about the logged in user
.. code-block:: pycon

    >>> user = client.user


### User's book shelves
    .. code-block:: pycon

    >>> shelves = client.user_shelves


Setup
-----

    .. code-block:: bash

    $ pip install git+git://github.com/jmargeta/goodreads.git

.. |build-status| image:: https://travis-ci.org/jmargeta/goodreads.svg?branch=master
   :target: https://travis-ci.org/jmargeta/goodreads
