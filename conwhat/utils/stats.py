"""
ConWhAt stats functions 
"""

# Author: John Griffiths
# License: simplified BSD

import os,sys,yaml

import numpy as np,networkx as nx, pandas as pd
import nibabel as nib, nilearn as nl

from dipy.io import Dpy
from dipy.tracking.utils import target_line_based

import indexed_gzip as igzip

from joblib import Parallel,delayed

from readers import igzip4dnii



abd = os.path.split(__file__)[0]  + '/../data'


def compute_vol_hit_stats(roi_file,vfms,bboxes,idxs,readwith='indexgzip',n_jobs=1,atlas_dir=None,atlas_name=None,run_type='sharedmem',joblib_cache_dir='/tmp'):
  """
  """

  print 'computing hit stats for roi %s' % roi_file

  roi_img = nib.load(roi_file)
  roi_dat = roi_img.get_data()

  if idxs == 'all': idxs = range(vfms.shape[0])

  # only read files with overlapping bounding boxes
  bbox_isol,bbox_propol = compute_roi_bbox_overlaps(bboxes,roi_file) #est_file)
  bbox_isol_idx = np.nonzero(bbox_isol)[0]
  idxsinbbox = [idx for idx in idxs if idx in bbox_isol_idx]

  if atlas_dir == None:
    atlas_dir = '%s/%s' %(abd,atlas_name)


  # compute hit stats for roi on atlas volumes
  if run_type == 'simple': 

    hstats = Parallel(n_jobs=n_jobs,temp_folder=joblib_cache_dir)\
            (delayed(hit_stats_for_vols)\
            (roi_dat,igzip4dnii(vfms.ix[idx]['nii_file'],
            vfms.ix[idx]['4dvolind'],atlas_name=atlas_name,atlas_dir=atlas_dir))\
            for idx in idxsinbbox)

    idxsused = idxsinbbox

  elif run_type == 'sharedmem':

    # Loop through each file, load in to memory, and spawn parallel jobs

    hstats,idxsused = [],[]

    unique_fs_inbbox = sorted(np.unique(vfms.ix[idxsinbbox]['nii_file']))
     
    for fname in unique_fs_inbbox:
  
      #if atlas_dir: 
      fpath = '%s/%s' %(atlas_dir,fname) #'%s/%s/%s' %(abd,atlas_name,fname)
      #else: 
      #  fpath = fname

      idxs_forthisf = vfms[vfms.nii_file == fname].index
    
      idxstorun = [idx for idx in idxs_forthisf if idx in idxsinbbox]

      volinds = vfms.ix[idxstorun]['4dvolind']
    
      # buffer (than the default size of 16KB).
      fobj = igzip.IndexedGzipFile(filename=fpath,spacing=4194304,
                                   readbuf_size=131072)

      # Create a nibabel image using 
      # the existing file handle.
      fmap = nib.Nifti1Image.make_file_map()
      fmap['image'].fileobj = fobj
      image = nib.Nifti1Image.from_file_map(fmap)
  
      vols = [np.squeeze(image.dataobj[:,:,:,int(v)]) for v in volinds]
    
      res = Parallel(n_jobs=n_jobs,temp_folder=joblib_cache_dir)\
           (delayed(hit_stats_for_vols)\
           (roi_dat,vol) for vol in vols)
               
      hstats += res
      idxsused += list(idxstorun)


  if len(hstats) > 0 :
    df_hstats = pd.DataFrame({idx: hstat for idx,hstat in zip(idxsused,hstats)}).T
    df_hstats.columns.names = ['metric'] 
    df_hstats.index.names = ['idx']
  else: 
    df_hstats = None

  return df_hstats


def hit_stats_to_nx(df_hit_stats,Gnx,vfms):
  """
  Put hit stats results into a networkx graph
  """
  Ghs = nx.Graph()

  for node,attrs in Gnx.node.items(): Ghs.add_node(node,attr_dict=attrs)

  for idx in df_hit_stats.index:
      dfi = df_hit_stats.ix[idx]
      vfm = vfms.ix[idx]
      roi1,roi2 = vfm['name'].split('_to_')
      roi1 = int(roi1); roi2 = int(roi2)
      Ghs.add_edge(roi1,roi2,attr_dict=dfi.to_dict())

  return Ghs






def hit_stats_calc(TP,TN,FP,FN):

  # Source: https://en.wikipedia.org/wiki/Confusion_matrix

  # Make sure divisions are by floats (classic python gotcha)
  TP = float(TP)
  TN = float(TN)
  FP = float(FP)
  FN = float(FN) 

  if TP == 0 and FN == 0:
    raise ValueError('TP = 0 and FN = 0; Test image is all zeros')

  # Condition positive
  P = TP + FN
    
  # Condition negative
  N = TN + FP
    
  # sensitivity / recall / hit rate / true positive rate (TPR)
  TPR = TP / (TP + FN)

  # specificity / true negative rate (TNR)
  TNR = TN / (FP + TN)
  
  # precision / positive predictive value (PPV)
  PPV = TP / (TP + FP)

  # negative predictive value (NPV)
  NPV = TN / (TN + FN)

  # fall-out / false positive rate (FPV)
  FPR = FP / (FP + TN)

  # false discovery rate (FDR)
  FDR = FP / (FP + TP) 

  # miss rate / false negative rate (FNR)
  FNR = FN / (FN + TP)
    
  # accuracy
  ACC = (TP + TN) / (P + N)
    
  # F1 score
  F1 = (2*TP) / (2*TP + FP + FN)
    
  # Matthews correlation coefficient (MCC)
  MCC = (TP*TN - FP*FN) / (np.sqrt((TP + FP)*(TP+FN)*(TN+FP)*(TN+FN)))
                           
  # Informedness / Bookmaker Informedness (BM)
  BM = TPR + TNR - 1
  
  # Markedness (MK)
  MK = PPV + NPV - 1


  # Cohen's kappa (c.f. Wakana et al. 2007; Wasserman et al. 2015)
  Nall  = TN + FP + FN + TN
  Enn   = (TN+FP)*(TN+FN) / Nall
  Enp   = (TN+FP)*(FP+TP) / Nall
  Epn   = Enp
  Epp   = (FN+TP)*(FP+TP) / Nall
  OA    = (TN + TP)   / Nall * 100.
  EA    = (Enn + Epp) / Nall  *100.
  Kappa = (OA-EA) / (100. - EA)
    

  RD = {'TPR': TPR, 'TNR': TNR,'PPV': PPV, 'NPV': NPV, 'FPR': FPR, 'FDR': FDR, 
        'FNR': FNR, 'ACC': ACC, 'F1': F1, 'MCC': MCC, 'BM': BM, 'MK': MK,
        'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN,'Kappa': Kappa}
  
  return RD



def hit_stats_for_vols(vol1,vol2, thr1=0,thr2=0):
    
  # Image 1 is the reference image
  # Image 2 is the image being tested

  #if type(vol1) == np.ndarray:
  #  dat1 = vol1
  #elif type(vol1) == str:    
  #  img1 = nib.load(vol1)
  #  dat1 = img1.get_data()
  #else: 
  #  img1 = vol1
  #  dat1 = img1.get_data()


  #if type(vol2) == np.ndarray:
  #  dat2 = vol2
  #elif type(vol2) == str:
  #  img2 = nib.load(vol2)
  #  dat2 = img2.get_data()
  #else:
  #  img2 = vol2
  #  dat2 = img2.get_data()

  dat1 = vol1
  dat2 = vol2
 
  dat1_thr = dat1.copy()
  dat1_thr[dat1_thr<thr1] = 0
    
  dat2_thr = dat2.copy()
  dat2_thr[dat2_thr<thr2] = 0
    
  dat1_thrbin = dat1_thr.copy()
  dat1_thrbin[dat1_thrbin>0] = 1
    
  dat2_thrbin = dat2_thr.copy()
  dat2_thrbin[dat2_thrbin>0] = 1

    
  thrbin_mul = dat1_thrbin*dat2_thrbin
    
  thrbininv_mul = (dat1_thrbin==0)*(dat2_thrbin==0)
  
  
  TP = thrbin_mul.sum()
  TN = thrbininv_mul.sum()
  FP = dat2_thrbin.sum()      - TP
  FN = (dat2_thrbin==0).sum() - TN
  
  res = hit_stats_calc(TP,TN,FP,FN)
    
  res['corr_nothr'] = np.corrcoef(dat1.ravel(),dat2.ravel())[0,1]
  res['corr_thr'] = np.corrcoef(dat1_thr.ravel(),dat2_thr.ravel())[0,1]
  res['corr_thrbin'] = np.corrcoef(dat1_thrbin.ravel(),dat2_thrbin.ravel())[0,1]
    
  return res




def get_bounding_box_inds(dat):
 
  if type(dat) == str: 
    if os.path.isfile(dat): 
      img = nib.load(dat)
      dat = img.get_data()

  if ((dat>0)).astype(float).sum()  > 0:
 
    nzx,nzy,nzz = np.nonzero(dat>0)
    xmin,xmax = nzx.min(),nzx.max()
    ymin,ymax = nzy.min(),nzy.max()
    zmin,zmax = nzz.min(),nzz.max()
    
    minmaxarr = np.array([[xmin,xmax],[ymin,ymax],[zmin,xmax]])    
    
    return minmaxarr

  else: 

    print 'no nonzero voxels'
    #return np.nan
    return [(np.nan,np.nan),(np.nan,np.nan),(np.nan,np.nan)]



def compute_roi_bbox_overlaps(bboxes,roi_file):
    
    roi_bbox = get_bounding_box_inds(roi_file)

    bbox_isol,bbox_propol = [],[]

    for ix in bboxes.index:

      bbox = bboxes.ix[ix].values

      if True in np.isnan(bbox): SI = 0.
      else:
        bbox = [[bbox[0],bbox[1]],[bbox[2],bbox[3]],[bbox[4],bbox[5]]]
        SI = get_intersection(roi_bbox,bbox)
      bbox_isol.append(SI!=0)
      bbox_propol.append(SI)

    return bbox_isol,bbox_propol

    
def get_intersection(bba,bbb):
    
  (xa1,xa2),(ya1,ya2),(za1,za2) = bba
  (xb1,xb2),(yb1,yb2),(zb1,zb2) = bbb
    
  SI = max(0, min(xa2,xb2) - max(xa1,xb1)) \
     * max(0, min(ya2,yb2) - max(ya1,yb1)) \
     * max(0, min(za2,zb2) - max(za1,zb1))

  return SI





def compute_streams_in_roi(roi_file,dpy_file,sfms,bboxes,idxs,n_jobs=1,atlas_name=None,joblib_cache_dir='/tmp'):

  #,idxs,readwith='indexgzip',n_jobs=1,atlas_name=None,run_type='sharedmem'):
  """
  """

  print 'computing hit stats for roi %s' % roi_file

  roi_img = nib.load(roi_file)
  roi_dat = roi_img.get_data()

  if idxs == 'all': idxs = range(sfms.shape[0])

  # DON'T DO BBOX STUFF YET...
  # only read files with overlapping bounding boxes
  bbox_isol,bbox_propol = compute_roi_bbox_overlaps(bboxes,roi_file) #est_file)
  bbox_isol_idx = np.nonzero(bbox_isol)[0]
  idxsinbbox = [idx for idx in idxs if idx in bbox_isol_idx]


  #def calc_streams_in_roi(dpy_file,roi_dat,stream_idxs):
  #  aff_eye = np.eye(4)
  #  D = Dpy(dpy_file, 'r')
  #  streams = D.read_tracksi(stream_idxs)
  #  D.close()
  #  streamsinroi = list(target_line_based(streams,roi_dat,aff_eye))
  #  return streamsinroi

  
  sir = Parallel(n_jobs=n_jobs,temp_folder=joblib_cache_dir)\
                (delayed(calc_streams_in_roi)\
                (dpy_file,roi_dat,sfms.ix[idx]['idxlist']) for idx in idxsinbbox)

  idxsused = idxsinbbox

  len_sir = [len(s) for s in sir]

  df = pd.DataFrame(len_sir, index=idxsused)
  df.columns = ['num_streams_in_roi']

  tot_streams = [sfms['idxlist'].ix[idx].shape[0] for idx in idxsused]

  df['tot_streams'] = tot_streams
  df['tot_streams_divnuminroi'] = df['tot_streams'] / df['num_streams_in_roi']
  df['pc_streams_in_roi'] = 100./df['tot_streams'] * df['num_streams_in_roi']
  df.index.names = ['idx']
  
  return df


def calc_streams_in_roi(dpy_file,roi_dat,stream_idxs):
  aff_eye = np.eye(4)
  D = Dpy(dpy_file, 'r')
  streams = D.read_tracksi(stream_idxs)
  D.close()
  streamsinroi = list(target_line_based(streams,roi_dat,aff_eye))
  return streamsinroi






def compute_vol_scalar_stats(params):

  print('computing vol scalar stats')
  raise NotImplementedError


def compute_stream_hit_stats(params):

  print('computing stream hit stats')
  raise NotImplementedError


def compute_stream_scalar_stats(params):

  print('computing stream scalar stats')
  raise NotImplementedError








