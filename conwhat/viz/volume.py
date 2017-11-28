"""
Utils for visualizing ConWhAt image volumes
"""

# Author: John Griffiths
# License: simplified BSD

import os,sys
import numpy as np
from itertools import product,combinations

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import nibabel as nib
from nilearn.plotting import plot_stat_map,cm as nl_cm
from nilearn.image import index_img
from nilearn.datasets import fetch_atlas_destrieux_2009
from nilearn.image import resample_to_img

from ..utils.stats import get_bounding_box_inds


# image volume plots

def plot_vol_scatter(vol,ax=None, pointint = 2,c='b',alpha=0.6,s=12.,
                     xlim=[0,100],ylim=[0,100],zlim=[0,100],marker='o',figsize=(20,20),
                     linewidth=0.05,show_bb=True,bb=None,bg_img=None,
                     bg_params = {'alpha': 0.5,'s': 20.,'linewidth': 0.005,'marker':'.', 'c': 'k'},
                     bg_pointint=15): 

  if type(vol) == str: 
    if os.path.isfile(vol):
      img = nib.load(vol)
      dat = img.get_data()
  elif type(vol) == nib.Nifti1Image:
    img = vol
    dat = img.get_data()
  else: 
    Exception('image file type not recognized')

  
  xs,ys,zs = np.nonzero(dat>0)    
  idx = np.arange(0,xs.shape[0])#,pointint)

  if not ax: 
    fig = plt.figure(figsize=figsize)
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')
    ax.set_xlim([xlim[0],xlim[1]])  
    ax.set_ylim([ylim[0],ylim[1]])
    ax.set_zlim([zlim[0],zlim[1]])

  ax.scatter3D(xs[idx],ys[idx],zs[idx],c=c,alpha=alpha,s=s, marker=marker,linewidths=linewidth)
   

  if bg_img == 'nilearn_destrieux':
    dest = fetch_atlas_destrieux_2009()
    bg_img = resample_to_img(nib.load(dest['maps']),
                             img,interpolation='nearest')
  if bg_img != None:
    
    bg_dat = bg_img.get_data()
    xs,ys,zs = np.nonzero(bg_dat>0)
    idx = np.arange(0,xs.shape[0],bg_pointint)
    ax.scatter3D(xs[idx],ys[idx],zs[idx],**bg_params)


  if show_bb:

    if bb == None:

      bb = get_bounding_box_inds(dat)

    if len(bb) == 6:
      xmin,xmax,ymin,ymax,zmin,zmax = bb
    elif bb.shape == (3,2):
      [[xmin,xmax],[ymin,ymax],[zmin,zmax]] = bb
    else: 
      Exception('Bounding box not recognized')

    corners = np.array(list(product([xmin,xmax],
                                    [ymin,ymax],
                                    [zmin,zmax])))
    cornerpairs = list(combinations(corners,2))

    linestoplot = [(s,e) for (s,e) in cornerpairs \
                   if ((np.abs(s-e) == 0).sum() == 2)]

    for (s,e) in linestoplot:
      ax.plot3D(*zip(s,e), color=c)


  return ax




def plot_vol_nilearn(vol,ax=None, pointint = 2,c='b',alpha=0.6,s=12.,
                     xlim=[0,100],ylim=[0,100],zlim=[0,100],marker='o',figsize=(20,20),
                     linewidth=0.05,show_bb=True,bb=None,bg_img=None,
                     bg_params = {'alpha': 0.5,'s': 20.,'linewidth': 0.005,'marker':'.', 'c': 'k'},
                     bg_pointint=15):

  if type(vol) == str:
    if os.path.isfile(vol):
      img = nib.load(vol)
      dat = img.get_data()
  elif type(vol) == nib.Nifti1Image:
    img = vol
    dat = img.get_data()
  else:
    Exception('image file type not recognized')



def plot_vol_and_rois_nilearn(vol,labels,roi1_img=None,roi2_img=None,
                              roi1=None,roi2=None,ax=None):

  if type(vol) == str:
    if os.path.isfile(vol):
      img = nib.load(vol)
      dat = img.get_data()
  elif type(vol) == nib.Nifti1Image:
    img = vol
    dat = img.get_data()
  else:
    Exception('image file type not recognized')



  if type(labels) == str:
    if os.path.isfile(labels):
      labels_img = nib.load(labels)
      labels_dat = labels_img.get_data()
  elif type(labels) == nib.Nifti1Image:
    labels_img = labels
    labels_dat = labels_img.get_data()
  else:
    Exception('labels file type not recognized')

  if labels is not None:
 
    roi1_img = nib.Nifti1Image((labels_img.get_data() == roi1).astype(float),
                             labels_img.affine)
  
    roi2_img = nib.Nifti1Image((labels_img.get_data() == roi2).astype(float),
                             labels_img.affine)


  display = plot_stat_map(img,cmap='hot',dim=5)#,threshold=0.2,dim=5)

  display.add_overlay(roi1_img,cmap=nl_cm.black_blue,vmax=3.)
  display.add_overlay(roi2_img,cmap=nl_cm.green_transparent,vmax=3.)


  return display

    
def plot_vol_cnxn():
  ""

  raise NotImplementedError

def plot_vol_tract():

  raise NotImplementedError