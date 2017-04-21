"""
ConWhAt Nipype Workflow Tests
"""


from nipype import config, logging
config.enable_debug_mode()
logging.update_logging(config)


# Test make_sub_visitation_map_workflow:


# ...


# Test make_group_visitation_map workflow:

from conwhat.construct import create_group_visitation_map_wf


sub_vismap_base_dir = '/u1/work/hpc3230/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc33'
sub_vismap_fstr = sub_vismap_base_dir + '/{subject_id}/vismap_{subject_id}_{cnxn_name}_std.nii.gz'


cnxns_list = '/u1/work/hpc3230/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc33/group/vismap_grp_cnxns_list.txt'
cnxn_names = [r[:-1] for r in open(cnxns_list,'r').readlines()]
#cnxn_names = ['0-10', '10-35']

#subs = [105620,105923,106016,106319]
allhcpsubs = [r[:-1] for r in open('/u1/work/hpc3230/ConWhAt/code/HCP_900.txt', 'r').readlines()]
subs = allhcpsubs[:700]

group_vismap_fstr = 'vismap_grp_{cnxn_name}.nii.gz'




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wf_name = 'CW_l2k8sc33_group_visitation_maps_shorttest'
gwf_shorttest = create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names[10:12],subs[:30],
                                               group_vismap_fstr,wf_name)
gwf_shorttest.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'
gwf_shorttest.run()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wf_name = 'CW_l2k8sc33_group_visitation_maps_longtest'
gwf_longtest = create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names,subs,
                                               group_vismap_fstr,wf_name)
gwf_longtest.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'
gwf_longtest.run()



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#config.disable_debug_mode()


wf_name = 'CW_l2k8sc33_group_visitation_maps_shorttest_qsub'
gwf_shorttest_qsub = create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names[10:12],subs[:30],
                                               group_vismap_fstr,wf_name)
gwf_shorttest_qsub.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'

plugin_args = {'qsub_args': '-q abaqus.q ',  # '-l nodes=1:ppn=3', 
               'overwrite': True,
               'dont_resubmit_completed_jobs': True,
               'template': 'qsub_template.sh'}

gwf_shorttest_qsub.run(plugin='SGEGraph', plugin_args=plugin_args)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


wf_name = 'CW_l2k8sc33_group_visitation_maps_shorttest_qsub2'
gwf_shorttest_qsub2 = create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names[10:20],subs[:80],
                                               group_vismap_fstr,wf_name)
gwf_shorttest_qsub2.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'

plugin_args = {'qsub_args': '-q abaqus.q ',  # '-l nodes=1:ppn=3', 
               'overwrite': True,
               'dont_resubmit_completed_jobs': True,
               'template': 'qsub_template.sh'}


gwf_shorttest_qsub2.run(plugin='SGEGraph', plugin_args=plugin_args)





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


wf_name = 'CW_l2k8sc33_group_visitation_maps_longtest_qsub'
gwf_longtest_qsub = create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names,subs,
                                               group_vismap_fstr,wf_name)
gwf_longtest_qsub.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'

plugin_args = {'qsub_args': '-q abaqus.q ',  # '-l nodes=1:ppn=3', 
               'overwrite': True,
               'dont_resubmit_completed_jobs': True,
               'template': 'qsub_template.sh'}


gwf_longtest_qsub.run(plugin='SGEGraph', plugin_args=plugin_args)







# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sub_vismap_base_dir_sc60 = '/u1/work/hpc3230/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc60'
sub_vismap_fstr_sc60 = sub_vismap_base_dir_sc60 + '/{subject_id}/vismap_{subject_id}_{cnxn_name}_std.nii.gz'


cnxns_list = '/u1/work/hpc3230/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc60/group/vismap_grp_cnxns_list.txt'
cnxn_names = [r[:-1] for r in open(cnxns_list,'r').readlines()]
#cnxn_names = ['0-10', '10-35']

#subs = [105620,105923,106016,106319]
allhcpsubs = [r[:-1] for r in open('/u1/work/hpc3230/ConWhAt/code/HCP_900.txt', 'r').readlines()]
subs = allhcpsubs[:700]

group_vismap_fstr = 'vismap_grp_{cnxn_name}.nii.gz'


wf_name = 'CW_l2k8sc60_group_visitation_maps_longtest_qsub'

gwf_longtest_qsub_sc60 = create_group_visitation_map_wf(sub_vismap_fstr_sc60,cnxn_names,subs,
                                                   group_vismap_fstr,wf_name)
gwf_longtest_qsub_sc60.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'

plugin_args = {'qsub_args': '-q abaqus.q ',  # '-l nodes=1:ppn=3',
               'overwrite': True,
               'dont_resubmit_completed_jobs': True,
               'template': 'qsub_template.sh'}


gwf_longtest_qsub_sc60.run(plugin='SGEGraph', plugin_args=plugin_args)







# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sub_vismap_base_dir_sc125 = '/u1/work/hpc3230/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc125'
sub_vismap_fstr_sc125 = sub_vismap_base_dir_sc125 + '/{subject_id}/vismap_{subject_id}_{cnxn_name}_std.nii.gz'


cnxns_list = '/u1/work/hpc3230/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc125/group/vismap_grp_cnxns_list.txt'
cnxn_names = [r[:-1] for r in open(cnxns_list,'r').readlines()]
#cnxn_names = ['0-10', '10-35']

#subs = [105620,105923,106016,106319]
allhcpsubs = [r[:-1] for r in open('/u1/work/hpc3230/ConWhAt/code/HCP_900.txt', 'r').readlines()]
subs = allhcpsubs[:700]

group_vismap_fstr = 'vismap_grp_{cnxn_name}.nii.gz'


wf_name = 'CW_l2k8sc125_group_visitation_maps_longtest_qsub'

gwf_longtest_qsub_sc125 = create_group_visitation_map_wf(sub_vismap_fstr_sc125,cnxn_names,subs,
                                                   group_vismap_fstr,wf_name)
gwf_longtest_qsub_sc125.base_dir = '/u1/work/hpc3230/conwhat_atlases/nipype'

plugin_args = {'qsub_args': '-q abaqus.q ',  # '-l nodes=1:ppn=3',
               'overwrite': True,
               'dont_resubmit_completed_jobs': True,
               'template': 'qsub_template.sh'}


gwf_longtest_qsub_sc125.run(plugin='SGEGraph', plugin_args=plugin_args)







