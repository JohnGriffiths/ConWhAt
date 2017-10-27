"""
Utils for reading ConWhAt and external data files
"""

# Author: John Griffiths
# License: simplified BSD

import os,sys,yaml,h5py

import numpy as np,networkx as nx, pandas as pd
import nibabel as nib, nilearn as nl
from nibabel.affines import apply_affine
from dipy.io import Dpy
import indexed_gzip as igzip



# Atlas base dir

abd = os.path.split(__file__)[0]  + '/../data'




def load_vol_file_mappings(atlas_name=None,atlas_dir=None):

  print  'loading file mapping'

  if atlas_dir == None: atlas_dir = os.path.join(abd,atlas_name)

  mappings = pd.read_csv(atlas_dir + '/mappings.txt', sep=',')

  return mappings,atlas_dir


def load_vol_bboxes(atlas_name=None,atlas_dir=None):

  print  'loading vol bbox'

  if atlas_dir == None: atlas_dir = os.path.join(abd,atlas_name)

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
    name = vfm['name']

    # Allow either '33-55' or '33_to_55' naming conventions
    if '_to_' in name:
      roi1,roi2 = name.split('_to_')
    else:
      roi1,roi2 = name.split('-')

    roi1 = int(roi1); roi2 = int(roi2)
    ad = vfm.to_dict()
    ad.update(bboxes.ix[idx])

    ad['idx'] = idx
    ad['weight'] = weights[roi1,roi2]

    n1,n2 = G.node[roi1]['attr_dict'],G.node[roi2]['attr_dict']

    # (ibid...)
    if '_to_' in name:
      fullname = n1['region_label'] + '_to_' + n2['region_label']
    else:
      fullname = n1['region_label'] + '-' + n2['region_label']

    ad['fullname'] = fullname


    G.add_edge(roi1,roi2,attr_dict=ad)
    

  return G




def load_stream_file_mappings(atlas_name=None,atlas_dir=None):

  print  'loading streamline file mappings'

  if not atlas_dir: atlas_dir = os.path.join(abd,atlas_name)

  F = h5py.File(atlas_dir + '/mappings.h5', 'r')
  KVs = {k: v.value for k,v in F.items()}
  F.close()
  mappings = pd.DataFrame(np.array(KVs.values()),
                             index=KVs.keys())
  mappings.columns = ['idxlist']
  mappings.index.names = ['name']
  mappings = mappings.reset_index()

  return mappings,atlas_dir


def load_stream_file_mappings_multifile(atlas_name=None,atlas_dir=None):

  print  'loading mult-file streamline file mappings'

  if not atlas_dir: atlas_dir = os.path.join(abd,atlas_name)

  # Difference from above is that the keys are now (sub,cnxn), rather than cnxn
  F = h5py.File(atlas_dir + '/mappings_multifile.h5', 'r')
  KVs = {k: v.value for k,v in F.items()}
  F.close()
  mappings = pd.DataFrame(np.array(KVs.values()),
                             index=KVs.keys())
  mappings.columns = ['idxlist']
  mappings.index.names = ['sub','name']
  mappings = mappings.reset_index()

  return mappings,atlas_dir





# (this is identical to load vox bboxes. Remove both
#  and replace with single func?)
def load_stream_bboxes(atlas_name=None,atlas_dir=None):

  print  'loading stream bbox'

  if not atlas_dir: atlas_dir = os.path.join(abd,atlas_name)

  bbox = pd.read_csv(atlas_dir + '/bounding_boxes.txt', sep=',',
                     names=['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'])

  return bbox



def make_streams_nx_graph(sfms,bboxes,weights,region_labels,hemis,cortex):

  


  # I THINK THIS CAN BE THE SAME FUNC FOR BOTH \
  # VOLUMETRIC AND STREAMLINETRIC
  # ...just writing one for streamlines first to get clear...


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
  for idx in sfms.index:
    sfm = sfms.ix[idx]
    name = sfm['name']

    # Allow either '33-55' or '33_to_55' naming conventions
    if '_to_' in name:
      roi1,roi2 = name.split('_to_')
    else: 
      roi1,roi2 = name.split('-')

    roi1 = int(roi1); roi2 = int(roi2)
    ad = sfm.to_dict()
    ad.update(bboxes.ix[idx])

    ad['idx'] = idx
    ad['weight'] = weights[roi1,roi2]

    n1,n2 = G.node[roi1],G.node[roi2]

    # (ibid...)
    if '_to_' in name: 
      fullname = n1['region_label'] + '_to_' + n2['region_label']
    else: 
      fullname = n1['region_label'] + '-' + n2['region_label']

    ad['fullname'] = fullname


    G.add_edge(roi1,roi2,attr_dict=ad)





def igzip4dnii(fname,inds3d,
               inds0d='all',inds1d='all',inds2d='all',
               atlas_name=None,
               atlas_dir=None):

  # If atlas dir given, file is assumed to be in there
  if atlas_dir:
    fname = '%s/%s' %(atlas_dir,fname)
  else:
    # If atlas dir not given but atlas name is given, assumes path is relative 
    # to local conwhat atlas dir
    if atlas_name: 
      fname = '%s/%s/%s' %(abd,atlas_name,fname)

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
    
  

  if inds3d == 'N/A' or np.isnan(inds3d):
    dims0,dims1,dims2 = image.shape
    dat = np.squeeze(image.dataobj[:,:,:])

  else:

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


def dpy_to_trk(dpy_file,ref,outfile,inds='all'):
  
    if os.path.isfile(ref):
        ref_img = nib.load(ref)
    else: 
        ref_img = ref
        
    # Make trackvis header 
    hdr = nib.trackvis.empty_header()
    hdr['voxel_size'] = ref_img.get_header().get_zooms()   
    hdr['dim'] = ref_img.shape
    hdr['voxel_order'] = "LAS"#"RAS"
    hdr['vox_to_ras'] = ref_img.affine
    zooms = ref_img.header.get_zooms()

    # Load streamlines
    D = Dpy(dpy_file, 'r')
    if inds == 'all':
      dpy_streams = D.read_tracks()
    else:
      dpy_streams = D.read_tracksi(inds)
    D.close()
    
    # Convert to trackvis space + format
    [apply_affine(hdr['vox_to_ras'], s*zooms) for s in dpy_streams]    
    
    trk_streams = [(s,None,None) for s in dpy_streams]
    
    nib.trackvis.write(outfile,trk_streams,hdr)

