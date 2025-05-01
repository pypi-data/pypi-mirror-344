
Install
-------

.. code-block:: bash

    pip install saved_instance

Basic Usage
-----------

Alice.py

.. code-block:: python

    from saved_instance import simple_storage

    message_dict = simple_storage()

    message_dict["message"] = "Hello World"

Bob.py

.. code-block:: python

    from saved_instance import simple_storage

    message_dict = simple_storage()

    print(message_dict["message])