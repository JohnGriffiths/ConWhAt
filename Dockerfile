FROM continuumio/anaconda
LABEL maintainer "tom@maladmin.com"
LABEL maintainer "j.davidgriffiths@gmail.com"

# Ensure some packages never get installed
ADD Build/apt-preferences /etc/apt/preferences

# Run apt-get calls
RUN apt-get update \
  && apt-get install -y --no-install-suggests \
    git \
    wget

# Add the neurodebian repos
RUN wget -O- http://neuro.debian.net/lists/jessie.us-nh.full | tee /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-key adv --recv-keys --keyserver hkp://pgp.mit.edu:80 0xA5D32F012649A5A9


# install some atlases from FSL
RUN apt-get update \
  && apt-get install -y --no-install-suggests \
    fsl-atlases  \
    fsl-harvard-oxford-atlases \
    fsl-harvard-oxford-cortical-lateralized-atlas \
    fsl-juelich-histological-atlas \
    fsl-mni152-templates \
    fsl-neurosynth-atlas \
    fsl-neurosynth-top100-atlas \
	&& rm -rf /var/lib/apt/lists/*

# Setup the Jupyter environment
RUN /opt/conda/bin/conda install jupyter -y --quiet

# add some dependencies
RUN pip install nilearn

ADD ConWhAt/ /opt/ConWhAt/ConWhAt/
ADD config.yaml /opt/ConWhAt/config.yaml
ENV PYTHONPATH /opt/ConWhAt:$PYTHONPATH

ENTRYPOINT /opt/conda/bin/jupyter notebook --notebook-dir=/opt/ConWhAt/ConWhAt/scratch --ip='*' --port=8888 --no-browser
