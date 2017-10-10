
"""
Downloading NeuroImaging datasets: atlas datasets
"""
import os
from nilearn.datasets.utils import _fetch_files

def fetch_conwhat_atlas(data_dir=None, url=None, resume=True, verbose=1,
                        uncompress=True,dataset_name=None):
    """Downloads and unpacks ConWhAt atlases

    Parameters
    ----------
    data_dir: string
        directory where data should be downloaded and unpacked.

    url: string
        url of file to download.

    resume: bool
        whether to resumed download of a partly-downloaded file.

    verbose: int
        verbosity level (0 means no message).

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

    if url is None:

      if dataset_name == 'CWL2k8Sc33Vol3d100s':

        url = "https://www.nitrc.org/frs/download.php/10254/" \
              "CWL2k8Sc33Vol3d100s.zip"


    #opts = {'uncompress': uncompress}
    #files = [(dataset_name,url,opts)]
    #files_ = _fetch_files(data_dir,files,resume=resume,verbose=verbose)

    dataset_dir = '%s/%s' %(data_dir,dataset_name)

    
    if not os.path.isdir(dataset_dir):

      cwd = os.getcwd()
      os.chdir(data_dir) 
      data_file = url.split('/')[-1]
      
      if os.path.isfile(data_file):
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

      os.chdir(cwd)

    return dataset_dir








