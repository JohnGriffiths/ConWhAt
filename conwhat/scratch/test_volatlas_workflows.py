"""
VolAtlas Workflow Tests
"""

"""

1. Make cnxn mappings

2. Mini workflow test

- restricted sub group set
- restricted cnxn set

3. Full workflow test

"""


"""
Setup
"""

# Tests to run

make_cnxn_mappings = False # True
run_mini_test = False # True # True # False
run_medium_test = True  #  False # True

run_on_grid = True # False # True



# Importage


if run_on_grid == False:
  from nipype import config, logging
  config.enable_debug_mode()
  logging.update_logging(config)



import os,sys,glob,numpy as np
sys.path.append('/home/hpc3230/Code/libraries_of_mine/github/ConWhAt')
from conwhat.construct import create_volatlas_workflow


# Define some variables
ref_file = '/opt/fsl/5.0.9/fsl/data/standard/FMRIB58_FA_1mm.nii.gz'
outdir_base = '/scratch/hpc3230/conwhat_nipype_tests'


if run_on_grid == False:
  wf_base_dir = outdir_base + '/run_on_loginnode'
else:
  wf_base_dir = outdir_base  + '/run_on_grid'
if not os.path.isdir(wf_base_dir): os.makedirs(wf_base_dir)





mini_subject_list = ['111312','113821']
medium_subject_list = ['105620','120717', '136833', 
                        '164131', '188751', '205220',
	                '299154', '397861', '617748',
                        '735148', '865363']

cnxn_mapping_subject_list = medium_subject_list


#all_subs = [s[:-1] for s in open('/u1/work/hpc3230/ConWhAt/code/HCP_900.txt', 'r').readlines()]


dpy_fstr = '/u1/work/hpc3520/hcp_wuminn_l2k8_tracks_conmats/data/results/hcp_wuminn/tractography/dipy/l2k8/%s/dsi_sd4/tracks.dpy'
warp_fstr = '/u1/work/hpc3399/hcp_wuminn_JHU_wmms/data/results/%s/nat2std_warp.nii.gz'
parc_fstr = '/u1/work/hpc3399/hcp_wuminn_l2k8_parcs/data/results/l2k8_rois/%s/ROI_scale33_dwispace.nii.gz'
                
cnxn_mapping_dir = outdir_base + '/cnxn_mappings' 

cnxn_mapping_fstr = cnxn_mapping_dir + '/G_%s.h5'

qsub_template = '/home/hpc3230/Code/libraries_of_mine/github/ConWhAt/conwhat/scratch/qsub_template.sh'

import sys
sys.path.append('/home/hpc3230/Code/libraries_of_mine/github/ConWhAt')
from conwhat.construct.volatlas_functions import make_sub_cnxn_mappings

plugin_args = {'qsub_args': '-q abaqus.q ',  # '-l nodes=1:ppn=3',
               'overwrite': True,
               'dont_resubmit_completed_jobs': True,
               'template': qsub_template}




"""
1. Make cnxn mappings 
"""


if make_cnxn_mappings:

  print 'making cnxn mappings'

  if not os.path.isdir(cnxn_mapping_dir): os.makedirs(cnxn_mapping_dir)

  for sub in cnxn_mapping_subject_list:

    dpy_file = dpy_fstr %sub 
    parc_file =  parc_fstr %sub
    cnxn_inds_outfile,cnxn_lens_outfile,cnxn_mat_outfile = make_sub_cnxn_mappings(sub,dpy_file,parc_file,cnxn_mapping_dir)



"""
2. Mini workflow tests
"""

if run_mini_test:

  print 'running mini workflow test'

  wf_name = 'wf_mini_test'

  wf_dir = '%s/%s' %(wf_base_dir, wf_name)

  subject_list = mini_subject_list

  agg_cnxn_names_dict = {'grp_vismap_norm_cat_1': ['1-10','1-20','1-30', '1-40'],
                         'grp_vismap_norm_cat_2': ['2-10', '2-20', '2-30', '2-40'],
                         'grp_vismap_norm_cat_10': ['10-20', '10-30', '10-35', '10-40']}


  cnxn_names = []; 
  for v in agg_cnxn_names_dict.values(): cnxn_names+=v
  cnxn_names = list(np.unique(cnxn_names))

  fstr_dict = {'dpy': dpy_fstr, 'warp': warp_fstr, 'parc': parc_fstr, 'cnxn_mapping': cnxn_mapping_fstr}

  wf_mini = create_volatlas_workflow(wf_name,wf_dir,subject_list,cnxn_names,fstr_dict,ref_file,agg_cnxn_names_dict)

  if run_on_grid == True:
    wf_mini.run(plugin='SGEGraph', plugin_args=plugin_args)


"""
3. Medium workflow tests
"""
# All ROIs, 10 subjects


if run_medium_test: 
  print 'running medium workflow test'

  wf_name = 'wf_medium_test'

  wf_dir = '%s/%s' %(wf_base_dir,wf_name)

  subject_list = medium_subject_list

  agg_cnxn_names_dict = {}
  n_nodes = 84
  for n in range(1,n_nodes):
    agg_name = 'grp_vismap_norm_cat_%s' %n
    cnxn_names = ['%s-%s' %(n,nn) for nn in range(1,n_nodes)]
    agg_cnxn_names_dict[agg_name] = cnxn_names

  cnxn_names = []; 
  for v in agg_cnxn_names_dict.values(): cnxn_names+=v
  cnxn_names = list(np.unique(cnxn_names))

  fstr_dict = {'dpy': dpy_fstr, 'warp': warp_fstr, 'parc': parc_fstr, 'cnxn_mapping': cnxn_mapping_fstr}

  wf_medium = create_volatlas_workflow(wf_name,wf_dir,subject_list,cnxn_names,fstr_dict,ref_file,agg_cnxn_names_dict)

  if run_on_grid == True:
    wf_medium.run(plugin='SGEGraph', plugin_args=plugin_args)





