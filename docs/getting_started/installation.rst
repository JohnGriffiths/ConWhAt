============
Installation
============


Using latest github master source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone latest version from github

.. code::

    $ git clone https://github.com/JohnGriffiths/ConWhAt
    
    
Now go to the cloned folder and install manually 

 
.. code::

   $ cd ConWhAt
   $ python setup.py install

Alternatively, simply add the cloned path to your :code:`pythonpath`.


Using pypi
~~~~~~~~~~

*(coming soon)*


Using with docker
~~~~~~~~~~~~~~~~~

*(coming soon)*



- Install docker-engine `(instructions here) <https://docs.docker.com/engine/installation/>`_

- Build the docker container

.. code::

   $ docker build -it ConWhAt <path to ConWhAt folder>

- Start Jupyter notebook server in the container

.. code::

   $ docker run -it -p 8888:8888 ConWhAt

