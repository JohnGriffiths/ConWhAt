from nipype import config, logging
config.enable_debug_mode()
logging.update_logging(config)


# Test make_sub_visitation_map_workflow:


# ...


# Test make_group_visitation_map workflow:

sub_vismap_base_dir = '/mnt/hpcvl-u1/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc33'
sub_vismap_fstr = cnxn_base_dir + '/{subject_id}/vismap_{subject_id}_{cnxn_name}_std.nii.gz'

cnxn_names = ['0-10', '10-35']
subs = [105620,105923,106016,106319]

group_vismap_fstr = 'test_group_visitation_map_wf_{cnxn_name}.nii.gz'

wf_name = 'make_group_visitation_map_workflow'

gwf = create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names,subs,group_vismap_fstr,wf_name)

gwf.base_dir = '/tmp/test_conwhat_gwf'



gwf.run()
