"""
Atlas class definitions 
"""

# Author: John Griffiths
# License: simplified BSD

import os

from nilearn.image import index_img

from utils.readers import (load_connectivity,load_vol_file_mappings,load_vol_bboxes,
                           load_stream_file_mappings,load_stream_bboxes,
                           make_nx_graph)

from utils.stats import (compute_vol_hit_stats,compute_vol_scalar_stats,
                         compute_streams_in_roi,#compute_stream_hit_stats,compute_stream_scalar_stats,
                         hit_stats_to_nx)

#from viz.network import plot_network,plot_matrix
#from viz.volume import plot_vol_cnxn,plot_vol_tract
#from viz.streams import plot_stream_cnxn,plot_stream_tract






class _Atlas(): # object):
  """
  Base atlas class
  """

  def __init__(self):

    print 'blah'


class _VolAtlas(_Atlas):
  """
  Volumetric atlas class
  """

  def __init__(self,atlas_name=None,atlas_dir=None):

    self.atlas_name = atlas_name

    # Load volumetric atlas info

    #if atlas_dir:
    #  self.vfms,self.atlas_dir = load_vol_file_mappings(atlas_dir=atlas_dir)
    #  self.bbox = load_vol_bboxes(atlas_dir=atlas_dir)
    #else: 
    #  self.vfms,self.atlas_dir = load_vol_file_mappings(atlas_name=atlas_name) 
    #  self.bbox = load_vol_bboxes(atlas_name=atlas_name)
    self.vfms,self.atlas_dir = load_vol_file_mappings(atlas_name=atlas_name,atlas_dir=atlas_dir)
    self.bbox = load_vol_bboxes(atlas_name=atlas_name,atlas_dir=atlas_dir)



  def get_vol_from_vfm(self,idx):
    """ 
    Convenience method to return nifti volume for an entry in the vfm table
    """

    fname = self.vfms.ix[idx]['nii_file']
    vol = self.vfms.ix[idx]['4dvolind']
    
    if not os.path.isfile(fname):  
      
      candidate = os.path.join(self.atlas_dir,fname)
      if os.path.isfile(candidate): 
        fname = candidate
      else: 
          Exception('File not found')
    
    if os.path.isfile(fname):
      print 'getting atlas entry %s: volume %s from image file %s'  %(idx,vol,fname)
    img = index_img(fname,vol)
    
    return img

    

  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple'):
    """
    Compute hit stats and store inside this object
    under 'name'
    """

    df_hit_stats = compute_vol_hit_stats(roi,self.vfms,self.bbox,
                                      idxs,n_jobs=n_jobs,
                                      atlas_name=self.atlas_name,
                                      atlas_dir=self.atlas_dir)

    #G_hit_stats = hit_stats_to_nx(df_hit_stats,self.Gnx,self.vfms)
    #return df_hit_stats,G_hit_stats
    return df_hit_stats



  def compute_scalar_stats(self,params,name):
    """
    Compute scalar stats and store inside this 
    object under 'name'
    """

    res = compute_vol_scalar_stats(params)

    self.scalar_stats[name] = res



class VolTractAtlas(_VolAtlas):
  """
  Volumetric tract-based atlas base class
  """

  def __init__(self,atlas_name=None,atlas_dir=None):

    _VolAtlas.__init__(self,atlas_name=atlas_name,atlas_dir=atlas_dir)


  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple'):
    """
    Compute hit stats and store inside this object
      under 'name'
    """
  
    df_hit_stats = compute_vol_hit_stats(roi,self.vfms,self.bbox,
                                      idxs,n_jobs=n_jobs,
                                      atlas_name=self.atlas_name,
                                      atlas_dir = self.atlas_dir)
    return df_hit_stats



  def plot_tract(self,atlas_name):

    # (uses plotting param defaults tuned to JHU atlas)
    plot_tract()




class VolConnAtlas(_VolAtlas):
  """
  Volumetric connectivity-based atlas
  """

  def __init__(self,atlas_dir=None,atlas_name=None):

    _VolAtlas.__init__(self,atlas_dir=atlas_dir,atlas_name=atlas_name)

    # Load connectivity info

    ws,rls,tls,rxyzs,rnii,ctx,hs,rmfslh,rmfsrh = load_connectivity(atlas_name=atlas_name,atlas_dir=atlas_dir)
    
    self.weights = ws
    self.region_labels = rls

    if tls is not None: self.tract_lengths = tls
    if rxyzs is not None: self.region_xyzs = rxyzs
    if rnii is not None: self.region_nii = rnii
    if ctx is not None: self.cortex = ctx
    if hs is not None: self.hemispheres = hs
    if rmfslh is not None: self.region_mapping_fsav_lh = rmfslh
    if rmfsrh is not None: self.region_mapping_fsav_rh = rmfsrh

 
    # Compile node and connectivity info into a networkx graph
    self.Gnx = make_nx_graph(self.vfms,self.bbox,ws,rls,hs,ctx)



  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple'):
    """
    Compute hit stats and store inside this object
      under 'name'
    """

    df_hit_stats = compute_vol_hit_stats(roi,self.vfms,self.bbox,
                                      idxs,n_jobs=n_jobs,
                                      atlas_name=self.atlas_name,
                                      atlas_dir=self.atlas_dir)

    G_hit_stats = hit_stats_to_nx(df_hit_stats,self.Gnx,self.vfms)

    return df_hit_stats,G_hit_stats






  def get_vol_from_rois(self,roi1,roi2):

    g = self.Gnx[int(roi1)][int(roi2)]
    idx = g['idx']
    
    vfm = self.vfms.ix[idx]
    nii_file = vfm['nii_file']
    volnum = vfm['4dvolind']
    
    if not os.path.isfile(nii_file):
      candidate = os.path.join(self.atlas_dir,nii_file)
      if os.path.isfile(candidate):
        nii_file = candidate
      else: 
        Exception('file not found')
    
    if os.path.isfile(nii_file): img = index_img(nii_file,volnum)
   
    return img


  def modify_connectome(self, name='mc1',function=''):
    """
    Modify canonical connectome using hit or scalar 
    stats, and store in this obj
    """

    res = modify_vol_connectome()

    self.modcons[name] = res
   


  def plot_network(self):
   
    plot_network()


  def plot_matrix(self):

    plot_matrix()


  def nl_plot_cnxn_and_rois(self,roi1=None,roi2=None,idx=None):


    if roi1 and roi2:
      img = self.get_vol_from_rois(roi1,roi2)
    elif idx: 
      img = self.get_vol_from_idx(idx)
     

    





class _StreamAtlas(_Atlas):   
  """
  Streamlinetric atlas base class
  """
    
  def __init__(self,atlas_name=None,atlas_dir=None):

    self.atlas_name = atlas_name

    # Load streamlinetric atlas info

    self.sfms,self.atlas_dir = load_stream_file_mappings(atlas_name=atlas_name,atlas_dir=atlas_dir)
    self.bbox = load_stream_bboxes(atlas_name=atlas_name,atlas_dir=atlas_dir)

    self.dpy_file = '%s/atlas_streams.dpy' %(self.atlas_dir)


class StreamTractAtlas(_StreamAtlas):
  """
  Streamlinetric tract-based atlas base class
  """
  
  def __init__(self,atlas_name=None,atlas_dir=None):

    _StreamAtlas.__init__(self,atlas_name=atlas_name,atlas_dir=atlas_dir)


class StreamConnAtlas(_StreamAtlas):
  """
  Streamlinetric connectome-based atlas base class
  """

  def __init__(self,atlas_name=None,atlas_dir=None):
    # A lot of this is shared between StreamConn atlas and VolConn atlas. 
    # modify...

    _StreamAtlas.__init__(self,atlas_name=atlas_name,atlas_dir=atlas_dir)

    # Load connectivity info

    ws,rls,tls,rxyzs,rnii,ctx,hs,rmfslh,rmfsrh = load_connectivity(atlas_name=atlas_name,atlas_dir=atlas_dir)

    self.weights = ws
    self.region_labels = rls

    if tls is not None: self.tract_lengths = tls
    if rxyzs is not None: self.region_xyzs = rxyzs
    if rnii is not None: self.region_nii = rnii
    if ctx is not None: self.cortex = ctx
    if hs is not None: self.hemispheres = hs
    if rmfslh is not None: self.region_mapping_fsav_lh = rmfslh
    if rmfsrh is not None: self.region_mapping_fsav_rh = rmfsrh


    # Compile node and connectivity info into a networkx graph
    self.Gnx = make_nx_graph(self.sfms,self.bbox,ws,rls,hs,ctx)




  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple'):
    """
    Compute hit stats and store inside this object
    under 'name'
    """

    df_hit_stats = compute_streams_in_roi(roi,self.dpy_file,self.sfms,self.bbox,
                                          idxs,n_jobs=n_jobs,
                                          atlas_name=self.atlas_name)

    G_hit_stats = hit_stats_to_nx(df_hit_stats,self.Gnx,self.sfms)

    return df_hit_stats,G_hit_stats







  def modify_connectome(self, name='mc1',function=''):
    """
    Modify canonical connectome using hit or scalar 
    stats, and store in this obj
    """

    res = modify_stream_connectome()

    self.modcons[name] = res
   


  def plot_network(self):
   
    plot_network()


  def plot_matrix(self):

    plot_matrix()


  def plot_cnxns(self):

    plot_stream_cnxns()



