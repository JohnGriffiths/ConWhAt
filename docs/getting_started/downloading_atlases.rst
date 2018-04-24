===================
Downloading atlases
===================

In order to use ConWhAt you will need to download the atlases you want to use in your analyses. 

Be aware: some of these files are quite large!

The atlas files are hosted on the `ConWhAt NITRC page <https://www.nitrc.org/projects/conwhat/>`_.

There are currently three options for downloading the atlas data:


1. Navigate to the NITRC page using the above link and download atlases manually
2. Use the links in the table below
3. Use the provided data fetcher utilities (see below)



List of ConWhAt atlases
-----------------------

Here is a list of the currently and soon-to-be available ConWhAt atlases:


+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
|         Name           |       Description                    | Available                                                                                 |
+========================+======================================+===========================================================================================+
| CWL2k8Sc33Vol3dS100    | Lausanne 2008 scale 33 parcellation  | *Now* `(link) <https://www.nitrc.org/frs/download.php/10381/CWL2k8Sc33Vol3d100s_v1.zip>`_ |
|                        | volumetric, 100subjects              |                                                                                           |
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc60Vol3dS100    | Lausanne 2008 scale 60 parcellation  | *Now* `(link) <https://www.nitrc.org/frs/download.php/10381/CWL2k8Sc60Vol3d100s_v1.zip>`_ |
|                        | volumetric, 100subjects              |                                                                                           |
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc125Vol3dS100   | Lausanne 2008 scale 125 parcellation | *Soon*                                                                                    |
|                        | volumetric, 100subjects              |                                                                                           | 
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc250Vol3dS100   | Lausanne 2008 scale 250 parcellation | *Soon*                                                                                    | 
|                        | volumetric, 100subjects              |                                                                                           | 
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc500Vol3dS100   | Lausanne 2008 scale 500 parcellation | *Soon*                                                                                    |
|                        | volumetric, 100subjects              |                                                                                           | 
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc33StreamS100   | Lausanne 2008 scale 33 parcellation  | *Soon*                                                                                    |
|                        | streamlinetric, 100subjects          |                                                                                           | 
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc60StreamS100   | Lausanne 2008 scale 60 parcellation  | *Soon*                                                                                    |
|                        | streamlinetric, 100subjects          |                                                                                           |
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc125StreamS100  | Lausanne 2008 scale 125 parcellation | *Soon*                                                                                    |
|                        | streamlinetric, 100subjects          |                                                                                           |
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc250StreamS100  | Lausanne 2008 scale 250 parcellation | *Soon*                                                                                    |
|                        | streamlinetric, 100subjects          |                                                                                           |
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+
| CWL2k8Sc500StreamS100  | Lausanne 2008 scale 500,parcellation | *Soon*                                                                                    |
|                        | streamlinetric, 100subjects          |                                                                                           | 
+------------------------+--------------------------------------+-------------------------------------------------------------------------------------------+


Downloading using the data fetcher functions
---------------------------------------------

Atlases can be downloaded directly from the NITRC repository
using the `fetcher` utilities:

.. code-block:: python

    from conwhat.utils.fetchers import fetch_conwhat_atlas

    res = fetchers.fetch_conwhat_atlas(atlas_name='CWL2k8Sc33Vol3d100s_v01',
                                       dataset_dir='/tmp',remove_existing=True)




Note on streamlinetric atlases
---------------------------------------------

Important note: the streamlinetric atlases all make use of a common streamlines file, which is quite large 
and only needs to be downloaded once. Currently that file lives in the L2k8 scale 33 atlas folder. 
You need to create symlinks to that file in all other streamlinetric atlas folders that use that 
streamlines file. Downloading using the data fetcher (recommended) will set up these hyperlinks for you. 









