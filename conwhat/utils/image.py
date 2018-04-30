
import nibabel as nib

import numpy as np
from numpy import pi,sin,cos

from nipy.labs.spatial_models.discrete_domain import grid_domain_from_image

from scipy.spatial import cKDTree
from scipy import ndimage
from scipy.ndimage.morphology import binary_dilation
from scipy.ndimage import binary_fill_holes




def ellipsoid_roi(center, radii, rotation, base_img):


        if type(rotation) == list:
          rotation = get_combined_rotation_matrix(rotation)


        # Make ellipsoid
        
        u = np.linspace(0.0, 2.0 * np.pi, 100)
        v = np.linspace(0.0, np.pi, 100)
        
        # cartesian coordinates that correspond to the spherical angles:
        x = radii[0] * np.outer(np.cos(u), np.sin(v))
        y = radii[1] * np.outer(np.sin(u), np.sin(v))
        z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
        # rotate accordingly
        for i in range(len(x)):
            for j in range(len(x)):
                [x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + center
 

        # Make ROI
    
        base_img_dom = grid_domain_from_image(base_img)
        
        XYZ = np.array([x.ravel(),y.ravel(),z.ravel()])
        XYZT = XYZ.T
        nearest_inds = cKDTree(base_img_dom.coord).query(XYZT, k=1)[1]
        mask_dat = np.zeros_like(base_img.get_data())
        mask_ijks = base_img_dom.ijk[nearest_inds,:]

        for i,j,k in mask_ijks:
            mask_dat[i,j,k] = 1


        # Dilate once, and fill holes. 
        mask_dat = binary_dilation(mask_dat)
        mask_dat = binary_fill_holes(mask_dat)
        mask_dat_img = nib.Nifti1Image(mask_dat.astype(int),base_img.affine)    
    
        return mask_dat_img,XYZT
    
    
def get_rotation_matrix(rotation_axis, deg):
    
  '''Return rotation matrix in the x,y,or z plane'''
   
  
 
  # (note make deg minus to change from anticlockwise to clockwise rotation)
  th = -deg * (pi/180.) # convert degrees to radians
    
  if rotation_axis == 0:
    return np.array( [[    1.,         0,         0    ],
                      [    0,      cos(th),   -sin(th)],
                      [    0,      sin(th),    cos(th)]])
  elif rotation_axis ==1:
    return np.array( [[   cos(th),    0,        sin(th)],
                      [    0,         1.,          0    ],
                      [  -sin(th),    0,        cos(th)]])
  elif rotation_axis ==2:
    return np.array([[   cos(th),  -sin(th),     0    ],
                     [    sin(th),   cos(th),     0   ],
                     [     0,         0,          1.   ]])

def get_combined_rotation_matrix(rotations):
  '''Return a combined rotation matrix from a dictionary of rotations around 
     the x,y,or z axes'''
  rotmat = np.eye(3)
    
  if type(rotations) is tuple: rotations = [rotations] 
  for r in rotations:
    newrot = get_rotation_matrix(r[0],r[1])
    rotmat = np.dot(rotmat,newrot)
  return rotmat








