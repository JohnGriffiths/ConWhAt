=================
Using with docker
=================

(**deprecated**)



### Creating a docker container

- Install docker-engine [Instructions](https://docs.docker.com/engine/installation/)

- Build the docker container

`docker build -it ConWhAT <path to ConWhAT folder>`

- Start Jupyter notebook server in the container

`docker run -it -p 8888:8888 ConWhAT`

