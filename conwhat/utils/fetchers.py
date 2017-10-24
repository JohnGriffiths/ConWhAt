
"""
Downloading NeuroImaging datasets: atlas datasets
"""
import os
from nilearn.datasets.utils import _fetch_files

def fetch_conwhat_atlas(atlas_name,dataset_dir,resume=True, verbose=1,
                        uncompress=True,remove_existing=False):
    """Downloads and unpacks ConWhAt atlases

    Parameters
    ----------
    data_dir: string
        directory where data should be downloaded and unpacked.

    atlas_name: string
        name of atlas to download

    resume: bool
        whether to resumed download of a partly-downloaded file.

    verbose: int
        verbosity level (0 means no message).

    remove_existing: bool
        remove any existing folders in the target location before 
        downloading


    Returns
    -------
    data: folder name for conwhat atlas

    References
    ----------
    Licence: Creative Commons Attribution Non-commercial Share Alike
    http://creativecommons.org/licenses/by-nc-sa/2.5/

    Griffiths, J.D., & McIntosh, A.R. (in preparation)
    "Connectome-based white matter atlases for virtual lesion studies"

    """


    if not os.path.isdir(dataset_dir):
      print 'dataset dir not present. creating'
      os.makedirs(dataset_dir)

    if atlas_name == 'CWL2k8Sc33Vol3d100s_v01':
        url = "https://www.nitrc.org/frs/download.php/10381/CWL2k8Sc33Vol3d100s_v01.zip"
    elif atlas_name == 'CWL2k8Sc60Vol3d100s_v01':
        url = "https://www.nitrc.org/frs/download.php/10382/CWL2k8Sc60Vol3d100s_v01.zip"
    else: 
        raise NameError('requested atlas not recognized')

    atlas_dir = '%s/%s' %(dataset_dir,atlas_name)

    if os.path.isdir(atlas_dir):

      if remove_existing == True:
 
        print 'removing existing folder'
        os.system('rm -r %s' %atlas_dir)

      else: 

        raise NameError('output folder already present. aborting.')
     
    cwd = os.getcwd()
    os.chdir(dataset_dir) 
    data_file = url.split('/')[-1]
      
    if os.path.isfile(data_file):
      if remove_existing==True:
        print '\n\nduplicate file detected - removing...'
        cmd = 'rm %s' %data_file
        print '%s' %cmd
        os.system(cmd)

    print '\n\ndownloading data_file %s...' %data_file
    cmd = 'wget %s' %url
    print '%s' %cmd
    os.system(cmd)
 
    print '\n\nunzipping file...'
    cmd = 'unzip %s' %data_file
    print '%s' %cmd
    os.system(cmd)
    print '\n\nfinished unzipping.'

    os.chdir(cwd)

    return dataset_dir








