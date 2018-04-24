.. Read the Docs Template documentation master file, created by
   sphinx-quickstart on Tue Aug 26 14:19:49 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ConWhAt's documentation!
==================================================

ConWhAt is a tool for studying the effects of white matter damage on brain networks. 

The code is hosted on github: https://github.com/JohnGriffiths/ConWhAt/

It is written in python and draws strongly on the powerful functionality provided by 
other neuroimaging analysis tools in the nipy ecosystem for manipulation and 
visualization of nifti images and tractography streamlines. 

The primary intended mode of interaction is through jupyter notebooks and python / 
bash scripting. Notebooks versions of some of the following documentation pages
can be viewed at https://github.com/JohnGriffiths/ConWhAt/doc/examples

( Please note: the software and atlases are still in beta, and future versions may 
include major front and/or backend changes )


.. toctree::
   :maxdepth: 1
   :caption: About ConWhAt
    
   overview.rst
   ontology_and_representation
   conwhat_atlases



.. toctree::.chat
   :maxdepth: 1
   :caption: Getting Started 

   installation.rst 
   getting_started.rst
   downloading_atlases.rst 
   getting_started.rst
   exploring_the_atlases.rst 
   exploring_the_canonical_connectomes.rst
  

.. toctree:: 
   :maxdepth: 1
   :caption: Analyses of Brain Lesions
  
   defining_a_lesion.rst
   compute_overlap.rst



.. toctree:: 
   :maxdepth: 1
   :caption: Other Applications
   
   connectivity_based_decomposition_of_white_matter_tracts.rst
   setting_up_tvb_simulations_from_conwhat_outputs.rst
   01_Downloading_ConWhAt_atlases.ipynb
   02_Exploring_ConWhAt_atlases.ipynb	
   03_Defining_a_lesion.ipynb
   04_Assess_network_impact_of_lesion.ipynb

   




