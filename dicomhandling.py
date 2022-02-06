# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#default angle en DcmRotate (exception?)



import os

import numpy as np

from PIL import Image

import pydicom as dicom

from scipy import ndimage as nd #aplicar el filtro gaussiano

class DcmFilter:
    
    def __init__(self, path, sigma=3):
        
        #a. Read and store a DICOM file’s pixel data as NumPy array.
        self.original = dicom.dcmread(path).pixel_array
        
        #b. Use a gaussian 2D filter to smooth the image with a default sigma of 3,
        #storing the resulting NumPy array.
        self.filtered = nd.gaussian_filter(self.original, sigma, mode='constant', cval=0.0)
        
        #c. Read the ImagePositionPatient DICOM tag and store it as a 3 item list.
        self.ipp = dicom.dcmread(path).ImagePositionPatient._list
   

class DcmRotate:
    def __init__(self, path, angle=180):
         
        #a. Read and store a DICOM file’s pixel data as NumPy array.
        self.original = DcmFilter(path).original
        
        #b. Rotate the image (multiples of 90º with a default angle of 180º), 
        #storing the resulting NumPy array.
        self.rotate = np.rot90(self.original,angle/90)
        
        #c. Read the ImagePositionPatient DICOM tag and store it as a 3 item list.
        self.ipp = DcmFilter(path).ipp
        
        
def check_ipp(dcm_filter, dcm_rotate):
        
        dcm_filter_ipp = dcm_filter.ipp
        dcm_rotate_ipp = dcm_rotate.ipp
    
        if dcm_filter_ipp == dcm_rotate_ipp:
            return True
        else:
            return False    
        
        
# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class IncorrectNumberOfImages(Error):
    """Raised when there are not 2 images"""
    pass
        
class SameImagePositionPatient(Error):
    """Raised when ipp is the same"""
    pass     
 
def main(input_folder):
    
        ld = os.listdir(input_folder)
        try:
            
            if len(ld) != 2:
                
                raise IncorrectNumberOfImages
            else:
                
                path1 = os.path.join(input_folder, ld[0])
                path2 = os.path.join(input_folder, ld[1])
                    
                dcm1 = DcmFilter(path1, 3)
                dcm2 = DcmFilter(path2, 3)
                
                try:
                    if check_ipp(dcm1,dcm2):
                        raise SameImagePositionPatient
                    
                    else: 
                        
                        original1 = dcm1.original
                        original2 = dcm2.original
                        
                        res1 = original1-original2
                        
                        filter1 = dcm1.filtered
                        filter2 = dcm2.filtered
                        
                        res2 = filter1-filter2
                        
                        output_dir = os.path.join(input_folder, 'residues')
                        os.mkdir(output_dir)
                        im1 = Image.fromarray(res1)
            
                        
                        im1.mode = 'I'
                        im1.point(lambda i:i*(1./256)).convert('L').save(os.path.join(output_dir, 'res1.jpeg'))
                  
                        im2 = Image.fromarray(res2)
                       
                        
                        im2.mode = 'I'
                        im2.point(lambda i:i*(1./256)).convert('L').save(os.path.join(output_dir, 'res2.jpeg'))
                  
                    
                except SameImagePositionPatient:
                     print("The DICOM files appear to be the same. Abborting.")
                     print()
 
        except IncorrectNumberOfImages:
            print("Incorrect number of images. Aborting.")
            print()

if __name__ == '__main__':
    main('images')


    
        
  
     
                
         




