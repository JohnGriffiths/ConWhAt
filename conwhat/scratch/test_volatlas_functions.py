# Test make_group_visitation_map() function:

from conwhat.construct import make_group_cnxn_visitation_map


print "\n\nCONWHAT TESTING: \n\n"


print "... 1: testing 'make group cnxn visitation map' function \n\n" 



sub_vismap_base_dir = '/global/home/hpc3230/u1/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc33'
sub_vismap_fstr = sub_vismap_base_dir + '/{subject_id}/vismap_{subject_id}_{cnxn_name}_std.nii.gz'

cnxns_list = '/global/home/hpc3230/u1/ConWhAt/data/results/visitation_maps/dipy_dsi_sd4_l2k8_sc33/group/vismap_grp_cnxns_list.txt'
cnxn_names = [r[:-1] for r in open(cnxns_list,'r').readlines()]

allhcpsubs = [r[:-1] for r in open('/global/home/hpc3230/u1/ConWhAt/code/HCP_900.txt', 'r').readlines()]
#subs = allhcpsubs[:700]
subs=allhcpsubs[:40]

cnxn_name = cnxn_names[10]
sub_vismaps = [sub_vismap_fstr.format(subject_id=sub,cnxn_name=cnxn_name) for sub in subs]
#grp_vismap = '/tmp/test_grp_vismap_%s.nii.gz' %cnxn_name
grp_vismap_fstr = '/tmp/test_grp_vismap_%s.nii.gz' # %cnxn_name

#make_group_visitation_map(cnxn_name,sub_vismaps,grp_vismap,subs_list=subs)
make_group_cnxn_visitation_map(cnxn_name,sub_vismaps,grp_vismap_fstr,subs_list=subs)












print "... 2: testing 'make sub cnxn visitation map' function \n\n" 




# Test make_sub_visitation_maps() function:

#from conwhat.construct import make_sub_visitation_maps
from conwhat.construct import make_sub_cnxn_visitation_maps

sub = 105620
dpy = '/global/home/hpc3520/u1/hcp_wuminn_l2k8_tracks_conmats/data/results/hcp_wuminn/tractography/dipy/l2k8/105620/dsi_sd4/tracks.dpy'
#dpy = '/tmp/tracks.dpy'
parc = '/global/home/hpc3399/u1/hcp_wuminn_l2k8_parcs/data/results/l2k8_rois/105620/ROI_scale33_dwispace.nii.gz'
warp = '/global/home/hpc3399/u1/hcp_wuminn_JHU_wmms/data/results/105620/nat2std_warp.nii.gz'
ref = '/opt/fsl/5.0.9/fsl/data/standard/FMRIB58_FA_1mm.nii.gz'
outdir = '/tmp/conwhat_msvm_test'


#make_sub_visitation_maps(sub,dpy,parc,warp,ref,outdir)

make_sub_cnxn_visitation_maps(sub,dpy,parc,warp,ref,outdir)



