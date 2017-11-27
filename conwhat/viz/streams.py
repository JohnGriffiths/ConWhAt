"""
Utils for visualizing ConWhAt streamlines
"""

# Author: John Griffiths
# License: simplified BSD


import os



def get_track_vis_pic(trk_file, length=None,bg_image=None,bz=None, sc='/tmp/movie_frame',
                      roi1_file=None,roi2_file=None,
                      bo=None,bc='0 0 0',tr=None,azim=0,elev=0,aa=False,
                      tc=None,showbox=False):
    
  """
  length = 
  bg_image = 
  bz = 
  sc = 
  rois = 
  b0 = 
  bc = 
  tr = 
  
  """
  #track_vis tracks.trk -l 20 -b recon_dwi.img -bz 1
  #track_vis tracks.trk -l 20 -sc movie/frame.png 1    
  
    
  # remove tmp.cam from current directory, if it's there
  if os.path.isfile('tmp.cam'): 
    print 'removing tmp.cam'
    os.system('rm tmp.cam')
    
  cmd = 'track_vis ' + trk_file
  if length: cmd+= ' -l %s' %length
  if bg_image: cmd+= ' -b ' + bg_image
  if bz: cmd+= ' -bz %s ' %bz
  if sc: cmd+= ' -sc %s.png 1'  %sc
                
  cmd+= ' -bc ' + bc
                    
  if roi1_file: 
    cmd+= ' -rois %s' %roi1_file
    if roi2_file: 
      cmd+= ' %s' %roi2_file

  if bo:
    cmd+= ' -sf %s 0.1 ' %bo
    
  if tr: 
    cmd += ' -s -r %s' %tr
    
  if tc:
    cmd += ' -c %s ' %tc
  if aa: cmd+= ' -aa '
       
  if showbox: cmd+= ' -box ' 
    
  cmd+= ' -camera azimuth %s elevation %s' %(azim,elev)
      
  cmd+= ' -na '
        
  print '\ntrack_vis call: \n\n%s' %cmd
            
  #res = %system $cmd         
  #print '\n\nres: \n\n%s ' %res          
  os.system(cmd)



def plot_stream_cnxn():

  print('plotting streamlinetric connection')
  raise NotImplementedError


def plot_stream_tract():

  print('plotting streamlinetric tract')
  raise NotImplementedError


