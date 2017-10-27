=============================
Exploring The ConWhAt Atlases
=============================

There are four different atlas types in ConWhat, corresponding to the 2
ontology types (Tract-based / Connectivity-Based) and 2 representation
types (Volumetric / Streamlinetric).

(More on this schema
`here <http://conwhat.readthedocs.io/en/latest/about_conwhat/ontology_and_representation.html>`__)

.. code:: ipython2

    # ConWhAt stuff
    from conwhat import VolConnAtlas,StreamConnAtlas,VolTractAtlas,StreamTractAtlas
    from conwhat.viz.volume import plot_vol_scatter
    
    # Neuroimaging stuff
    import nibabel as nib
    from nilearn.plotting import plot_stat_map,plot_surf_roi
    
    # Viz stuff
    %matplotlib inline
    from matplotlib import pyplot as plt
    import seaborn as sns
    
    # Generic stuff
    import glob, numpy as np, pandas as pd, networkx as nx

We'll start with the scale 33 lausanne 2008 volumetric
connectivity-based atlas.

Define the atlas name and top-level directory location

.. code:: ipython2

    atlas_dir = '/scratch/hpc3230/Data/conwhat_atlases'
    atlas_name = 'CWL2k8Sc33Vol3d100s_v01'

Initialize the atlas class

.. code:: ipython2

    vca = VolConnAtlas(atlas_dir=atlas_dir + '/' + atlas_name,
                       atlas_name=atlas_name)


.. parsed-literal::

    loading file mapping
    loading vol bbox
    loading connectivity


This atlas object contains various pieces of general information

.. code:: ipython2

    vca.atlas_name




.. parsed-literal::

    'CWL2k8Sc33Vol3d100s_v01'



.. code:: ipython2

    vca.atlas_dir




.. parsed-literal::

    '/scratch/hpc3230/Data/conwhat_atlases/CWL2k8Sc33Vol3d100s_v01'



Information about each atlas entry is contained in the ``vfms``
attribute, which returns a pandas dataframe

.. code:: ipython2

    vca.vfms.head()

