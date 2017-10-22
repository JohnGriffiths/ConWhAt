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


Alternatively, simply add the cloned path to you $pythonpath


Using pypi
~~~~~~~~~~

*(coming soon)*


Using with docker
~~~~~~~~~~~~~~~~~

*(coming soon)*

- Install docker-engine [Instructions](https://docs.docker.com/engine/installation/)

- Build the docker container

`docker build -it ConWhAt <path to ConWhAt folder>`

- Start Jupyter notebook server in the container

`docker run -it -p 8888:8888 ConWhAt`

