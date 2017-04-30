

from volatlas_functions import make_sub_cnxn_visitation_map
from volatlas_functions import make_group_cnxn_visitation_map
from volatlas_functions import aggregate_grp_vismap





def create_volatlas_workflow(wf_name,wf_base_dir,subject_list,cnxn_names,fstr_dict,ref_file,
                             agg_cnxn_names_dict):

  from nipype.pipeline import engine as pe
  from nipype.pipeline.engine import Node,JoinNode,MapNode,Workflow

  from nipype.pipeline.engine.utils import IdentityInterface
  from nipype.interfaces import Function

  from nipype.interfaces.io import DataSink


  """
  Variables
  """

  dpy_fstr = fstr_dict['dpy']
  warp_fstr= fstr_dict['warp']
  parc_fstr= fstr_dict['parc']
  cnxn_mapping_fstr = fstr_dict['cnxn_mapping']


  """
  Node: Infosource
  """
  # (iterates over subjects)
  def mirror(subject_id): return subject_id
  mirror_npfunc = Function(['subject_id'],['subject_id'],mirror)


  node__infosource = Node(interface=mirror_npfunc, name="infosource")
  node__infosource.iterables = [("subject_id",subject_list)]




  """
  Node: Get data
  """
  # (also iterates over cnxn ids)

  def get_sub_files_func(subject_id,cnxn_name,dpy_fstr,warp_fstr,parc_fstr,cnxn_mapping_fstr):
    dpy_file = dpy_fstr %subject_id
    cnxn_mapping_file = cnxn_mapping_fstr % subject_id
    parc_file = parc_fstr %subject_id
    warp_file = warp_fstr %subject_id
    
    return dpy_file,parc_file,warp_file,cnxn_mapping_file,cnxn_name,subject_id

  get_sub_files_npfunc = Function(['subject_id', 'cnxn_name','dpy_fstr', 'warp_fstr', 'parc_fstr', 'cnxn_mapping_fstr'],
                                  ['dpy_file', 'parc_file', 'warp_file', 
                                   'cnxn_mapping_file', 'cnxn_name', 'subject_id'],
                                   get_sub_files_func)


  node__datasource = Node(interface=get_sub_files_npfunc,
                          name='datasource')
  node__datasource.inputs.dpy_fstr = dpy_fstr
  node__datasource.inputs.parc_fstr = parc_fstr
  node__datasource.inputs.warp_fstr = warp_fstr
  node__datasource.inputs.cnxn_mapping_fstr = cnxn_mapping_fstr
  node__datasource.iterables = [('cnxn_name', cnxn_names)]




  """
  Node: Make sub cnxn visitation map
  """

  make_sub_vismap_npfunc = Function(['sub', 'dpy_file', 'parc_file', 'warp_file', 'ref_file', 'cnxn_inds_file', 
                                     'cnxn_name', 'vismap_fstr'],
                                     ['sub_vismap_file'],
                                      make_sub_cnxn_visitation_map)

  node__makesubvismap = Node(interface=make_sub_vismap_npfunc,
                             name="make_sub_vismap")


  node__makesubvismap.inputs.ref_file = ref_file
  node__makesubvismap.inputs.vismap_fstr = 'temp_vismap_%s.nii.gz'
  #node__makesubvismap.inputs.overwrite=True



  """
  Node: make grp cnxn visitation map
  """

  make_grp_vismap_npfunc = Function(['cnxn_name', 'sub_vismaps', 'grp_vismap_fstr', 'subs_list'],
                                    ['grp_vismap_fpath','grp_vismap_norm_fpath','subs_list_file'],
                                    make_group_cnxn_visitation_map)

  node__makegrpvismap = JoinNode(interface=make_grp_vismap_npfunc,
                                  name='make_grp_vismap',
                                  joinsource="infosource", 
                                  joinfield=["sub_vismaps", 'subs_list'])#subject_id")

  node__makegrpvismap.inputs.grp_vismap_fstr = 'grp_vismap_%s.nii.gz' # this needs to be changed to come from previous node in wf




  """
  Node: aggregate group cnxn visitation map
  """
  # (to do...)


  agg_grp_vismap_npfunc = Function(['in_files', 'cnxn_names', 'outfname'],
                                 ['agg_image_file', 'agg_list_file'],
                                 aggregate_grp_vismap, imports=['import os'])

  node__agggrpvismap = JoinNode(interface=agg_grp_vismap_npfunc,
                                name='agg_grp_vismap',
                                joinsource="datasource", 
                                joinfield=["in_files"])

  node__agggrpvismap.iterables = [("cnxn_names", agg_cnxn_names_dict.values()),
                                  ("outfname",   agg_cnxn_names_dict.keys())]
  node__agggrpvismap.synchronize = True
  



  """
  Node: datasink
  """
  # I want to use a mapnode for this, but can't get it to work
  # so have to settle with this followed by a command line copy...

  # (if you don't have a mapnode, just get same result as outputs of agggrpvismap node...)
  node__datasink = Node(DataSink(), name='datasink')
  node__datasink.inputs.base_directory = wf_base_dir

  #node__datasinkniifile = MapNode(DataSink(infields=['agg_image_file']),name='ds_nii', iterfield=['agg_image_file'])
  #node__datasinkniifile.inputs.base_directory=wf_base_dir
  #node__datasinktxtfile = MapNode(DataSink(infields=['agg_list_file']),name='ds_txt', iterfield=['agg_list_file'])
  #node__datasinktxtfile.inputs.base_directory=wf_base_dir



    
  """
  Workflow: put it all together
  """
 
  wf = pe.Workflow(name=wf_name)
  wf.base_dir = wf_base_dir

  wf.connect(node__infosource, 'subject_id', node__datasource, 'subject_id')
  wf.connect(node__datasource, 'subject_id',   node__makesubvismap, 'sub')
  wf.connect(node__datasource, 'dpy_file',   node__makesubvismap, 'dpy_file')
  wf.connect(node__datasource, 'parc_file',   node__makesubvismap, 'parc_file')
  wf.connect(node__datasource, 'warp_file',   node__makesubvismap, 'warp_file')
  wf.connect(node__datasource, 'cnxn_mapping_file',   node__makesubvismap, 'cnxn_inds_file')
  wf.connect(node__datasource, 'cnxn_name', node__makesubvismap, 'cnxn_name')
  wf.connect(node__makesubvismap, 'sub_vismap_file', node__makegrpvismap, 'sub_vismaps')
  wf.connect(node__datasource, 'cnxn_name', node__makegrpvismap, 'cnxn_name')
  wf.connect(node__datasource, 'subject_id', node__makegrpvismap, 'subs_list')

  wf.connect(node__makegrpvismap, 'grp_vismap_norm_fpath', node__agggrpvismap, 'in_files')

  wf.connect(node__agggrpvismap, 'agg_image_file', node__datasink, '@agg_image_file')
  wf.connect(node__agggrpvismap, 'agg_list_file', node__datasink, '@agg_list_file')

  #wf.connect(node__agggrpvismap, 'agg_image_file', node__datasinkniifile, '@agg_image_file')
  #wf.connect(node__agggrpvismap, 'agg_list_file',  node__datasinktxtfile, '@agg_list_file')

  return wf



