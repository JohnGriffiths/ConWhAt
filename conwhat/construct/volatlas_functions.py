"""
======================================================
ConWhAt Volumetric Atlas Construction Functions
======================================================


JG 20/04/2017

"""


# Importage

import os
import numpy as np

from dipy.io import Dpy
from dipy.tracking.utils import density_map,connectivity_matrix

from nipype.interfaces.fsl import ApplyWarp

import nibabel as nib

from joblib import Parallel,delayed 


"""
Subject visitation maps
"""


def make_sub_visitation_maps(sub,dpy,parc,warp,ref,outdir):
    
  """
  Inputs:
  
    sub     - subject ID
    
    dpy     - dpy file
    
    parc    - parc file
    
    warp    - nat2std warp file
    
    ref     - ref file
    
    outdir  - output directory.  
              Will be created if not already present. 
    
  
  Creates:
  
    - Visitation maps (nifti files) for each connetion
    - Connections list file
  
  Returns:
  
    - 
    
  
  
  Usage: 
  
    ...
  
  """

  print '\n\nMaking visitation maps for sub %s' %sub
    
    
  # Connections list file
  cnxns_list_file = '%s/cnxns_%s.txt'  %(outdir,sub)

  # Connectivity matrix file
  conmat_file = '%s/conmat_%s.txt' %(outdir,sub)
    
  # Filename template for visitation map files    
  vismap_nat_str = '%s/vismap_%s_' %(outdir,sub) + '%s-%s_nat.nii.gz'
  vismap_std_str = vismap_nat_str.replace('_nat', '_std')
    
    
  # Create output directory if not already present
  if not os.path.isdir(outdir): os.makedirs(outdir)
    
  # Load tractography streamlines
  print '\nLoading dipy streamlines'
  D = Dpy(dpy, 'r')
  dpy_streams = D.read_tracks()
  D.close()

  # Load parcellation file
  parc_img = nib.load(parc)
  parc_dat = parc_img.get_data().astype(np.int)

  # (This is specific to the way the dpy files were saved)
  affine = np.eye(4)

  # Compute connectivity matrix and streamline labels
  print '\n...computing connectivity'
  M,G = connectivity_matrix(dpy_streams,parc_dat,affine=affine,
                            return_mapping=True,mapping_as_streamlines=True)

  # Save connections list
  F = open(cnxns_list_file, 'w')
  F.writelines(['%s %s\n' %(str(g[0]),str(g[1])) for g in G.keys()])
  F.close()
    
  # Save connectivity matrix
  np.savetxt(conmat_file, M)
    

    
  def make_and_warp_dmap(inlist):
        
    pair_it,(pair,fibs) = inlist
        
    print '...%s; %s-%s (%s of %s)' %(sub,pair[0],pair[1],pair_it+1,len(G.keys()))

    outfile_nat = vismap_nat_str %(pair[0],pair[1])
    outfile_std = vismap_std_str %(pair[0],pair[1])

    dm = density_map(fibs,parc_img.shape,affine=affine)
    dm_img = nib.Nifti1Image(dm.astype("int16"), parc_img.affine)
    dm_img.to_filename(outfile_nat)

    aw = ApplyWarp(in_file=outfile_nat,
                   out_file=outfile_std,
                   ref_file =ref,
                   field_file =warp)
    aw.run()
    
  alist = []
  for pair_it,(pair,fibs) in enumerate(G.items()): alist.append([pair_it,(pair,fibs)])
   
  for a in alist:
    make_and_warp_dmap(a)           
  #Parallel(n_jobs=4)(delayed(make_and_warp_dmap)(a) for a in alist)
    
    
    
  print '\nFinished making visitation maps for subject %s' %sub

        
        
        
        
    
"""
Group visitation maps
"""

   
def make_group_visitation_map(cnxn_name,sub_vismaps,grp_vismap_fname,subs_list):
  """
  
  Inputs:
  
    cnxn_name        - connection name
    
    sub_vismaps      - list of input filepaths
    
    grp_vismap       - output filepath
    
    subs_list        - list of subject IDs
    
    
  
  Creates files:
  
  
  
  
  Usage:
  
  
  """
    
  import os
  import numpy as np
  import nibabel as nib
    

  # remove any subs with data missing
  num_subs_orig = len(subs_list)
  for sub,vismap in zip(subs_list,sub_vismaps):
    if not os.path.isfile(vismap):
      sub_vismaps.remove(vismap)
      subs_list.remove(sub)
  num_subs = len(subs_list)

  if num_subs == 0:
    #raise ValueError('No subjects with this vismap file found')
    print '\n\nNo subjects with this vismap file found. Exiting.'

    return None,None,None #return grp_vismap_fpath,grp_vismap_norm_fpath,subs_list_file

  else:

    print '\n\nMaking group map for cnxn %s\n  (%s subs)' %(cnxn_name,num_subs)

    grp_vismap_fpath = os.path.abspath(grp_vismap_fname)
    grp_vismap_norm_fpath = os.path.abspath(grp_vismap_fname.replace('.nii.gz', '_norm.nii.gz'))

    subs_list_file = grp_vismap_fpath.replace('.nii.gz', '_subslist.txt')


 
    # Load reference image
    ref_img = nib.load(sub_vismaps[0])

    # Initialize group visitation map 
    grp_vismap_dat = np.zeros_like(ref_img.get_data()).astype('int16')

  
    for f_it, f in enumerate(sub_vismaps):
        
      print '...adding %s' %f

      # Read in subject map

      img = nib.load(f)
      dat = img.get_data()
      dat_bin = (dat>0).astype('int16')

      # Add to group map

      grp_vismap_dat += dat_bin


    # Visitation map normalized by number of subjects (i.e. mean)
    # (...note we use the original subject list count. The result 
    #  is a visitation probability, relative to the original number 
    #  of subject and vismap files supplied)

    grp_vismap_norm_dat = grp_vismap_dat / np.float32(num_subs_orig)

        
    # Write maps to file
    print '\nwriting group visitation map image to %s' %grp_vismap_fpath
    grp_vismap_img = nib.Nifti1Image(grp_vismap_dat,ref_img.affine)
    grp_vismap_img.to_filename(grp_vismap_fpath)
  
    print '\nwriting subnum-normalized group visitation map image to %s' %grp_vismap_norm_fpath
    grp_vismap_norm_img = nib.Nifti1Image(grp_vismap_norm_dat,ref_img.affine)
    grp_vismap_norm_img.to_filename(grp_vismap_norm_fpath)

  
    # Write subject list to file
    if subs_list != None:
      print 'writing subs list to %s' %subs_list_file
      open(subs_list_file, 'w').writelines([str(s) + '\n' for s in subs_list])


    print '\n\nFinished making group visitation map for cnxn %s' %cnxn_name

    return grp_vismap_fpath,grp_vismap_norm_fpath,subs_list_file



