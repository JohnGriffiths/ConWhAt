"""
Atlas class definitions 
"""

# Author: John Griffiths
# License: simplified BSD
from __future__ import print_function

import os

import numpy as np
import nibabel as nib

from nilearn.image import index_img

from nilearn.plotting import plot_glass_brain

from .utils.readers import (load_connectivity,load_vol_file_mappings,load_vol_bboxes,
                           load_stream_file_mappings,load_stream_bboxes,
                           make_nx_graph,dpy_to_trk)

from .utils.stats import (compute_vol_hit_stats,compute_vol_scalar_stats,
                         compute_streams_in_roi,#compute_stream_hit_stats,compute_stream_scalar_stats,
                         hit_stats_to_nx)

from .viz.network import plot_network, plot_matrix
from .viz.volume import plot_vol_cnxn, plot_vol_tract
from .viz.streams import plot_stream_cnxn, plot_stream_tract






class _Atlas(): # object):
  """
  Base atlas class
  """

  def __init__(self):

    print('blah')


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

    self.scalar_stats = dict()

  def get_vol_from_vfm(self,idx):		
    """ 		
    Convenience method to return nifti volume for an entry in the vfm table		
    """		
 	
    nii_file = self.vfms.ix[idx]['nii_file']		
    volnum = self.vfms.ix[idx]['4dvolind']		
    		
    if not os.path.isfile(nii_file):  		
      candidate = os.path.join(self.atlas_dir,nii_file)		
      if os.path.isfile(candidate): 		
        nii_file = candidate		
      else: 		
          Exception('File not found')		
    		
    if os.path.isfile(nii_file):		
      if (np.isnan(volnum) or volnum == 'nan'):		
        print('getting atlas entry {}: image file {} ' % (idx,nii_file))
        img = nib.load(nii_file)		
      else:		
        print('getting atlas entry {}: volume %s from image file {}' % (idx,volnum,nii_file))
        img = index_img(nii_file,volnum)		
 		
    return img


  

  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple',joblib_cache_dir='/tmp'):
    """
    Compute hit stats and store inside this object
    under 'name'
    """

    df_hit_stats = compute_vol_hit_stats(roi,self.vfms,self.bbox,
                                      idxs,n_jobs=n_jobs,
                                      atlas_name=self.atlas_name,
                                      atlas_dir=self.atlas_dir,
                                      run_type=run_type,
                                      joblib_cache_dir=joblib_cache_dir)

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




  def get_bbox_dimsizes(self):
    """
    Return lists of lengths between bounding box minima 
    and maxima

    Usage: 

    xdimsize,ydimsize,zdimsize = cw.get_bbox_dimsizes()
    """

    xdimsize = np.abs(self.bbox['xmax'] - self.bbox['xmin'])
    ydimsize = np.abs(self.bbox['ymax'] - self.bbox['ymin'])
    zdimsize = np.abs(self.bbox['zmax'] - self.bbox['zmin'])

    xdimsize = xdimsize.sort_values(ascending=False)
    ydimsize = ydimsize.sort_values(ascending=False)
    zdimsize = zdimsize.sort_values(ascending=False)

    return xdimsize,ydimsize,zdimsize





class VolTractAtlas(_VolAtlas):
  """
  Volumetric tract-based atlas base class
  """

  def __init__(self,atlas_name=None,atlas_dir=None):

    _VolAtlas.__init__(self,atlas_name=atlas_name,atlas_dir=atlas_dir)


  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple',joblib_cache_dir='/tmp'):
    """
    Compute hit stats and store inside this object
      under 'name'
    """
  
    df_hit_stats = compute_vol_hit_stats(roi,self.vfms,self.bbox,
                                      idxs,n_jobs=n_jobs,
                                      atlas_name=self.atlas_name,
                                      atlas_dir = self.atlas_dir,
                                      run_type=run_type,joblib_cache_dir=joblib_cache_dir)
    return df_hit_stats



  def plot_tract(self,atlas_name):

    # (uses plotting param defaults tuned to JHU atlas)
    # plot_tract()
    raise NotImplementedError




class VolConnAtlas(_VolAtlas):
  """
  Volumetric connectivity-based atlas
  """

  def __init__(self,atlas_dir=None,atlas_name=None):

    _VolAtlas.__init__(self,atlas_dir=atlas_dir,atlas_name=atlas_name)

    # Load connectivity info

    ws,rls,tls,rxyzs,rnii,ctx,hs,rmfslh,rmfsrh = load_connectivity(atlas_name=atlas_name,atlas_dir=atlas_dir)
    
    self.__weights = ws
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

    self.modcons = dict()


  @property
  def weights(self):
    """Connectivity weights matrix"""
    return self.__weights



  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple',joblib_cache_dir='/tmp'):
    """
    Compute hit stats and store inside this object
      under 'name'
    """

    df_hit_stats = compute_vol_hit_stats(roi,self.vfms,self.bbox,
                                      idxs,n_jobs=n_jobs,
                                      atlas_name=self.atlas_name,
                                      atlas_dir=self.atlas_dir,
                                      run_type=run_type,
                                      joblib_cache_dir=joblib_cache_dir)

    G_hit_stats = hit_stats_to_nx(df_hit_stats,self.Gnx,self.vfms)

    return df_hit_stats,G_hit_stats


  def get_rois_from_idx(self,idx):
    """
    Note: assumes that 'name' column in vfms is 
          of the form 'roi1_to_roi2'
    """
    roi1,roi2 = self.vfms.ix[idx]['name'].split('_to_')
    roi1 = int(roi1)
    roi2 = int(roi2)

    return roi1,roi2 

 

  def get_idx_from_rois(self,roi1,roi2):
    g = self.Gnx[int(roi1)][int(roi2)]
    idx = g['idx']
    return idx
 

  def get_vol_from_rois(self,roi1,roi2):

    idx = self.get_idx_from_rois(roi1,roi2)
   
    img = self.get_vol_from_vfm(idx)

    """
    vfm = self.vfms.ix[idx]
    nii_file = vfm['nii_file']
    volnum = vfm['4dvolind']
    
    if not os.path.isfile(nii_file):
      candidate = os.path.join(self.atlas_dir,nii_file)
      if os.path.isfile(candidate):
        nii_file = candidate
      else: 
        Exception('file not found')
    
    if os.path.isfile(nii_file):
      if (np.isnan(volnum) or volnum == 'nan'):
        img = nib.load(nii_file)
      else:
        img = index_img(nii_file,volnum)
   
    return img
    """

    return img


  def modify_vol_connectome(self):

    raise NotImplementedError

  def modify_connectome(self, name='mc1',function=''):
    """
    Modify canonical connectome using hit or scalar 
    stats, and store in this obj
    """

    res = self.modify_vol_connectome()

    self.modcons[name] = res
   


  def plot_network(self):
   
    plot_network()


  def plot_matrix(self):

    plot_matrix()



  def get_single_roi_img(self,roinum):
    """
    Return nifti image with just this roi
    """
    
    roinum = int(roinum) 

    allrois_img = self.region_nii
    allrois_dat = allrois_img.get_data()

    thisroi_dat = (allrois_dat==roinum).astype('float32')
    thisroi_img = nib.Nifti1Image(thisroi_dat,allrois_img.affine)

    return thisroi_img



  def nl_plot_connvol(self,idx=None,roi1=None,roi2=None,add_rois=True,
                      nl_params = dict(threshold=0.1,cmap='Reds')):

    if idx: 
      cnxn_img = self.get_vol_from_vfm(idx)
      roi1,roi2 = self.get_rois_from_idx(idx)
    else:   
      cnxn_img = self.get_vol_from_rois(roi1,roi2)
 
    """
    if (roi1 != None) and (roi2 != None):

      roi1 = int(roi1)
      roi2 = int(roi2)

      str1 = '%s_to_%s' %(roi1,roi2)
      search1 = np.nonzero(vfms['name'] == str1)[0]

      str2 = '%s_to_%s' %(roi2,roi1)
      search2 = np.nonzero(vfms['name'] == str2)[0]

      if len(search1) > 0:
        idx = search1[0]
        cnxn_name = str1
      elif len(search2) > 0:
        idx = search2[0]
        cnxn_name = str2
      else:
        raise ValueError('connection not found')

    else:

      cnxn_name = vfms.ix[idx]['name']

      roi1 = int(vfms.ix[idx]['name'].split('_to_')[0])
      roi2 = int(vfms.ix[idx]['name'].split('_to_')[1])
    """

    display = plot_glass_brain(cnxn_img,**nl_params)

    if add_rois:

      roi1_img = self.get_single_roi_img(roi1)
      roi2_img = self.get_single_roi_img(roi2)

      display.add_contours(roi1_img, colors='Blue', linewidths=0.5, alpha=0.9)
      display.add_contours(roi2_img, colors='Green', linewidths=0.5, alpha=0.9)

    return display








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


  def write_subset_to_trk(self,ref_file,outfile,stream_inds='all'):

    print('writing streams to trk file: {}' % outfile)
    dpy_to_trk(self.dpy_file,ref_file,outfile,inds=stream_inds)




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

    self.__weights = ws
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

    self.modcons = dict()



  def get_rois_from_idx(self,idx):
    """
    Note: assumes that 'name' column in vfms is 
          of the form 'roi1_to_roi2'
    """
    roi1,roi2 = self.sfms.ix[idx]['name'].split('_to_')
    roi1 = int(roi1)
    roi2 = int(roi2)

    return roi1,roi2


  def get_idx_from_rois(self,roi1,roi2):
    g = self.Gnx[int(roi1)][int(roi2)]
    idx = g['idx']
    return idx



  def compute_hit_stats(self,roi,idxs,n_jobs=1,run_type='simple',joblib_cache_dir='/tmp'):
    """
    Compute hit stats and store inside this object
    under 'name'
    """

    df_hit_stats = compute_streams_in_roi(roi,self.dpy_file,self.sfms,self.bbox,
                                          idxs,n_jobs=n_jobs,
                                          atlas_name=self.atlas_name,
                                          joblib_cache_dir=joblib_cache_dir)

    G_hit_stats = hit_stats_to_nx(df_hit_stats,self.Gnx,self.sfms)

    return df_hit_stats,G_hit_stats





  def modify_stream_connectome(self):
    raise NotImplementedError

  def modify_connectome(self, name='mc1',function=''):
    """
    Modify canonical connectome using hit or scalar 
    stats, and store in this obj
    """

    res = self.modify_stream_connectome()

    self.modcons[name] = res
   


  def write_cnxn_to_trk(self,ref_file,outfile,idx=None,roi1=None,roi2=None):

    if not idx: 
      idx = self.get_idx_from_rois(roi1,roi2)
       
    idxlist = self.sfms.ix[idx]['idxlist']

    self.write_subset_to_trk(ref_file,outfile,stream_inds=idxlist)



  def plot_network(self):
   
    plot_network()


  def plot_matrix(self):

    plot_matrix()


  def plot_cnxns(self):

    plot_stream_cnxn()



