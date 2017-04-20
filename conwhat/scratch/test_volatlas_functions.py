# Test make_group_visitation_map() function:

fstr = '/mnt/hpcvl-u1/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc33/%s/vismap_%s_%s_std.nii.gz'

cnxn_name = '0-10'
grp_vismap = '/tmp/test_grp_vismap_%s.nii.gz' %cnxn_name
subs_list = [105620,105923,106016,106319]
sub_vismaps = [ fstr%(sub,sub,cnxn_name) for sub in subs_list]


make_group_visitation_map(cnxn_name,sub_vismaps,grp_vismap,subs_list=subs_list)


# Test make_sub_visitation_maps() function:

sub = 105620
#dpy = '/mnt/jzhpcvl-u1/hcp_wuminn_l2k8_tracks_conmats/data/results/hcp_wuminn/tractography/dipy/l2k8/105620/dsi_sd4/tracks.dpy'
dpy = '/tmp/tracks.dpy'
parc = '/mnt/mkhpcvl-u1/hcp_wuminn_l2k8_parcs/data/results/l2k8_rois/105620/ROI_scale33_dwispace.nii.gz'
warp = '/mnt/mkhpcvl-u1/hcp_wuminn_JHU_wmms/data/results/105620/nat2std_warp.nii.gz'
ref = '/usr/share/fsl/data/standard/FMRIB58_FA_1mm.nii.gz'
outdir = '/tmp/conwhat_msvm_test'


make_sub_visitation_maps(sub,dpy,parc,warp,ref,outdir)


