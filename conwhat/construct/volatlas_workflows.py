"""
======================================================
ConWhAt Volumetric Atlas Construction Nipype Workflows
======================================================

JG 20/04/2017
"""

from nipype.pipeline import engine as pe

from nipype.interfaces import Function

from . import make_group_visitation_map

"""
Subject visitation maps
"""

def create_sub_visitation_map_wf():
  print 'blah'
    


"""
Group visitation maps
"""


def create_group_visitation_map_wf(sub_vismap_fstr,cnxn_names,subs,grp_vismap_fstr,wf_name):
    
  
  # Node: get vismap files
    
  def get_filenames(sub_vismap_fstr,cnxn_name,subs,grp_vismap_fstr):
    import os
    # Get list of subject vismap filenames
    sub_vismap_flist = []
    for sub in subs:

      f = sub_vismap_fstr.format(subject_id=sub,cnxn_name=cnxn_name)
      
      # not doing this if-test here as this is now done inside the main function
      # (because we need to have the full sub list in the main function to do 
      #  normalization.
      #if not os.path.isfile(f):
      #  #raise ValueError('error - subject visitation map missing: %s' %f)
      #  print '
      #else:

      sub_vismap_flist.append(f)

    # Get group vismap filename
    grp_vismap_fname = grp_vismap_fstr.format(cnxn_name=cnxn_name)            
        
    return sub_vismap_flist,grp_vismap_fname,cnxn_name


  datasource = pe.Node(interface=Function(input_names=['sub_vismap_fstr', 'cnxn_name', 'subs', 'grp_vismap_fstr'],
                                          output_names = ['sub_vismap_flist', 'grp_vismap_fname', 'cnxn_name'],
                                          function=get_filenames),
                       name='datasource')
  datasource.inputs.sub_vismap_fstr = sub_vismap_fstr
  datasource.inputs.subs = subs
  datasource.inputs.grp_vismap_fstr = grp_vismap_fstr
  datasource.iterables = ('cnxn_name',cnxn_names)
        
        
        
  # Node: Make group visitation map
        
  make_gvm = pe.Node(interface=Function(input_names=['cnxn_name','sub_vismaps',
                                                     'grp_vismap_fname','subs_list'],
                                        output_names=['grp_vismap_fpath','grp_vismap_norm_fpath', 'subs_list_file'],
                                        function=make_group_visitation_map),
                     name='make_group_visitation_map')
  make_gvm.inputs.subs_list = subs

        

  # (can't currently get datasink node to work properly. Will just copy output files instead.)
  # Node: datasink

  #datasink = pe.Node(DataSink(), name='datasink')
  #datasink.inputs.base_directory = '/tmp/test_datasink_basedir' #path/to/output'
  #datasink.parameterization = False      
        
        
  # Create workflow
    
  wf = pe.Workflow(wf_name)
  wf.connect(datasource, 'sub_vismap_flist', make_gvm, 'sub_vismaps')
  wf.connect(datasource, 'grp_vismap_fname', make_gvm, 'grp_vismap_fname')
  wf.connect(datasource, 'cnxn_name', make_gvm, 'cnxn_name')
    
  #wf.connect(make_gvm,'grp_vismap_fpath',datasink, 'grp_vismaps')
  #wf.connect(make_gvm,'subs_list_file', datasink, 'grp_vismaps.@subslistfile')
  
  return wf


