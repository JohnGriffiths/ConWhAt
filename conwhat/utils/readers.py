"""
Utils for reading ConWhAt and external data files
"""

# Author: John Griffiths
# License: simplified BSD

import os,sys,yaml

import numpy as np,networkx as nx, pandas as pd
import nibabel as nib, nilearn as nl
import indexed_gzip as igzip



# Atlas base dir

abd = os.path.split(__file__)[0]  + '/../data'




def load_vol_file_mappings(atlas_name=None,atlas_dir=None):

  print  'loading file mapping'

  if not atlas_dir: atlas_dir = os.path.join(abd,atlas_name)

  mappings = pd.read_csv(atlas_dir + '/mappings.txt', sep=',')

  return mappings,atlas_dir


def load_vol_bboxes(atlas_name=None,atlas_dir=None):

  print  'loading vol bbox'

  if not atlas_dir: atlas_dir = os.path.join(abd,atlas_name)

  bbox = pd.read_csv(atlas_dir + '/bounding_boxes.txt', sep=',')

  return bbox




def load_connectivity(atlas_name=None,atlas_dir=None,weights_name='weights'):

  print 'loading connectivity'

  if not atlas_dir: atlas_dir = os.path.join(abd,atlas_name)


  # Mandatory files

  ws_file = '%s/%s.txt' %(atlas_dir,weights_name)
  rls_file = '%s/region_labels.txt' % atlas_dir

  ws = np.loadtxt(ws_file)
  rls = [l[:-1] for l in open(rls_file, 'r').readlines()]
  
 
  # Optional files
  
  tls_file = '%s/tract_lengths.txt' % atlas_dir
  rxyzs_file = '%s/region_xyzs.txt'  % atlas_dir
  rnii_file = '%s/region_masks.nii.gz' % atlas_dir
  hs_file = '%s/hemispheres.txt' % atlas_dir
  ctx_file = '%s/cortex.txt' % atlas_dir
  rmfslh_file = '%s/region_mapping_fsav_lh.txt' % atlas_dir
  rmfsrh_file = '%s/region_mapping_fsav_rh.txt' % atlas_dir  
   
  tls,rxyzs,rnii,ctxi,hs,rmfslh,rmfsrh = None,None,None,None,None,None,None

  if os.path.isfile(tls_file):    itls = np.loadtxt(tls_file)
  if os.path.isfile(rxyzs_file):  rxyzs = np.loadtxt(rxyzs_file)
  if os.path.isfile(rnii_file):   rnii = nib.load(rnii_file)
  if os.path.isfile(hs_file):     hs = np.loadtxt(hs_file)
  if os.path.isfile(ctx_file):    ctx = np.loadtxt(ctx_file)
  if os.path.isfile(rmfslh_file): rmfslh =np.loadtxt(rmfslh_file)
  if os.path.isfile(rmfsrh_file): rmfsrh = np.loadtxt(rmfsrh_file)


  return ws,rls,tls,rxyzs,rnii,ctx,hs,rmfslh,rmfsrh



def make_nx_graph(vfms,bboxes,weights,region_labels,hemis,cortex):

   
  G = nx.Graph()

  # add node info
  for node_it,node in enumerate(region_labels):

    rl = region_labels[node_it]
    hemi = hemis[node_it]
    ctx = cortex[node_it]

    G.add_node(node_it, attr_dict={'region_label': rl,
                                   'hemisphere': hemi,
                                   'cortex': ctx})

  # add edge info
  for idx in vfms.index:
    vfm = vfms.ix[idx]
    roi1,roi2 = vfm['name'].split('_to_')
    roi1 = int(roi1); roi2 = int(roi2)
    ad = vfm.to_dict()
    ad.update(bboxes.ix[idx])

    ad['idx'] = idx
    ad['weight'] = weights[roi1,roi2]

    n1,n2 = G.node[roi1],G.node[roi2]
    fullname = n1['region_label'] + '_to_' + n2['region_label']
    ad['fullname'] = fullname

    G.add_edge(roi1,roi2,attr_dict=ad)
    

  return G



def load_stream_file_mappings(atlas_name=None,atlas_dir=None):

  print 'loading stream file mappings'


def load_stream_bboxes(atlas_name=None,atlas_dir=None):

  print 'loading stream bbox'



def igzip4dnii(fname,inds3d,
               inds0d='all',inds1d='all',inds2d='all',
               atlas_name=None):

  # If atlas name is given, assumes path is relative 
  # to local conwhat atlas dir
  if atlas_name: fname = '%s/%s/%s' %(abd,atlas_name,fname)

  # Here we are usin 4MB spacing between
  # seek points, and using a larger read
  # buffer (than the default size of 16KB).
  fobj = igzip.IndexedGzipFile(
               filename=fname,#'big_image.nii.gz',
               spacing=4194304,
               readbuf_size=131072)
    
  # Create a nibabel image using 
  # the existing file handle.
  fmap = nib.Nifti1Image.make_file_map()
  fmap['image'].fileobj = fobj
  image = nib.Nifti1Image.from_file_map(fmap)
    
    
  # Use the image ArrayProxy to access the  
  # data - the index will automatically be
  # built as data is accessed.
 
  dims0,dims1,dims2,dims3 = image.shape
  #if inds0d == 'all': inds0d = range(dims0)
  #if inds1d == 'all': inds1d = range(dims1)
  #if inds2d == 'all': inds2d = range(dims2) 

  dat = np.squeeze(image.dataobj[:,:,:,int(inds3d)]) 
  #dat = np.squeeze(image.dataobj[inds0d,inds1d,inds2d,int(inds3d)])
  #if type(inds3d) == int: # len(inds3d) == 1:
  #  dat = np.squeeze(image.dataobj[inds0d,inds1d,inds2d,int(inds3d)])
  #else:
  #  dat = np.array([(image.dataobj[inds0d,inds1d,inds2d,int(i3)]) for i3 in inds3d])
  #  dat = dat.reshape([dims[1],dims[2],dims[3],dims[0]])
    
  return dat


