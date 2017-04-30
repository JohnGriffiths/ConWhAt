



def make_sub_cnxn_mappings(sub,dpy_file,parc_file,outdir,overwrite=True):

  import os,h5py,numpy as np,nibabel as nib
  from dipy.io import Dpy
  from dipy.tracking.utils import connectivity_matrix,length
    
  if not os.path.isdir(outdir): os.makedirs(outdir)

  cnxn_inds_outfile = '%s/G_%s.h5' %(outdir,sub)
  cnxn_lens_outfile = '%s/L_%s.h5' %(outdir,sub)
  cnxn_mat_outfile = '%s/M_%s.txt' %(outdir,sub)

  if overwrite == True: 
    for f in [cnxn_inds_outfile, cnxn_lens_outfile, cnxn_mat_outfile]:
      if os.path.isfile(f):
        print 'file exists (%s). Removing...' %f
        os.system('rm %s' %f)
        

  print '...loading streamlines'
  D = Dpy(dpy_file, 'r')
  dpy_streams = D.read_tracks()
  D.close()


  print '...loading parcellation'
  parc_img = nib.load(parc_file)
  parc_dat = parc_img.get_data().astype(np.int)

  affine = np.eye(4)

  print '...computing connectivity'
  M,G = connectivity_matrix(dpy_streams,parc_dat,affine=affine,
                            return_mapping=True,mapping_as_streamlines=False)

  print '...computing lengths'
  L = {k: list(length([dpy_streams[vv] for vv in v])) for k,v in G.items()}


  print '...writing cnxn inds to file'
  F = h5py.File(cnxn_inds_outfile, 'a')
  for k,v in G.items():  F['%s-%s' %(k[0],k[1])] = v
  F.close()

  print '...writing cnxn lens to file'
  F = h5py.File(cnxn_lens_outfile, 'a')
  for k,v in L.items():  F['%s-%s' %(k[0],k[1])] = v
  F.close()

  print '...writing connectivity matrix to file'
  np.savetxt(cnxn_mat_outfile,M)


  return cnxn_inds_outfile,cnxn_lens_outfile,cnxn_mat_outfile


def make_sub_cnxn_visitation_map(sub,dpy_file,parc_file,warp_file,ref_file,
                                 cnxn_inds_file,cnxn_name,vismap_fstr):
    
  overwrite=True
    
  import os,h5py,numpy as np,nibabel as nib
  from dipy.io import Dpy
  from dipy.tracking.utils import connectivity_matrix,length,density_map
  from nipype.interfaces.fsl import ApplyWarp    
       
  F = h5py.File(cnxn_inds_file, 'r')
  if cnxn_name in F.keys():
    stream_idxs = F[cnxn_name].value
    F.close()

    D = Dpy(dpy_file, 'r')
    streams = D.read_tracksi(stream_idxs)
    D.close()

    parc_img = nib.load(parc_file)

    affine = np.eye(4)


    outfile_nat = os.path.abspath('vismap_nat_%s.nii.gz' %cnxn_name)
    outfile_std =  os.path.abspath(vismap_fstr %cnxn_name)

    dm = density_map(streams,parc_img.shape,affine=affine)
    dm_img = nib.Nifti1Image(dm.astype("int16"), parc_img.affine)
    dm_img.to_filename(outfile_nat)

    print 'warping cnxn image to standard space'
    aw = ApplyWarp(in_file=outfile_nat,
                 out_file=outfile_std,
                 ref_file =ref_file,
                 field_file =warp_file)
    aw.run()

  else:
    outfile_std = 'cnxn not found'
    F.close()

  return outfile_std


def make_group_cnxn_visitation_map(cnxn_name,sub_vismaps,grp_vismap_fstr,subs_list):

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

    grp_vismap_fpath = os.path.abspath(grp_vismap_fstr %cnxn_name)
    grp_vismap_norm_fpath = grp_vismap_fpath.replace('.nii.gz', '_norm.nii.gz')

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




"""
Concatenate group visitation maps
"""

def aggregate_grp_vismap(in_files,cnxn_names,outfname):

  import os,sys,glob
  from nilearn.image import concat_imgs
  import nibabel as nib
    
    
  # Filter and order in files to match cnxn names list
  # Write aggregated vismap nifti file + text list of cnxn names
    
  # Note: need to make sure that cnxn name string doesn't acceidentally
  # identify the wrong files (e.g. 1-2 doesn't give 51-25)
  # ...do this by adding underscores before and after cnxn_name 
    
  agg_image_file = os.path.abspath(outfname + '.nii.gz')
  agg_list_file = agg_image_file.replace('.nii.gz', '_cnxn_list.txt')

  filtered_files,filtered_cnxns = [],[]
  for c in cnxn_names:
    for f in in_files:
      if f != None:
        if '_%s_' %c in f:
          filtered_files.append(f)
          filtered_cnxns.append(c)

  if len(filtered_cnxns) > 0:
            
    cat_img = concat_imgs(filtered_files)
     
    print '...writing concatenated nii to file %s' %agg_image_file
    cat_img.to_filename(agg_image_file)
        
    open(agg_list_file, 'w').writelines(['%s\n' %c for c in filtered_cnxns])
  

  else: 
        
    print 'no matching files found'
    agg_image_file,agg_list_file = 'N/A', 'N/A'
    
  return agg_image_file,agg_list_file          
        

