# -*- coding: utf-8 -*-
"""
R&D coding test

Alicia Pons Guinot
"""

#Import libraries

import os

import numpy as np

from PIL import Image

import pydicom as dicom #read cdm images

from scipy import ndimage as nd #gaussian filter


#Create a DcmFilter class
class DcmFilter:
    
    def __init__(self, path, sigma=3):
        
        #a. Read and store a DICOM file’s pixel data as NumPy array.
        self.original = dicom.dcmread(path).pixel_array
        
        #b. Use a gaussian 2D filter to smooth the image with a default sigma of 3,
        #storing the resulting NumPy array.
        self.filtered = nd.gaussian_filter(self.original, sigma, mode='constant', cval=0.0)
        
        #c. Read the ImagePositionPatient DICOM tag and store it as a 3 item list.
        self.ipp = dicom.dcmread(path).ImagePositionPatient._list
   

#Create a DcmRotate class
class DcmRotate:
    def __init__(self, path, angle=180):
         
        #a. Read and store a DICOM file’s pixel data as NumPy array.
        self.original = DcmFilter(path).original 
        #instead of repeating dicom.dcmread(path).pixel_array
        
        #b. Rotate the image (multiples of 90º with a default angle of 180º), 
        #storing the resulting NumPy array.
        self.rotate = np.rot90(self.original,angle/90)
        
        #c. Read the ImagePositionPatient DICOM tag and store it as a 3 item list.
        self.ipp = DcmFilter(path).ipp
        #instead of repeating dicom.dcmread(path).ImagePositionPatient._list
        
       
# Create check_ipp method. This code returns the bool "True" if both objects have the same ipp
def check_ipp(dcm_filter, dcm_rotate):
        
        dcm_filter_ipp = dcm_filter.ipp
        dcm_rotate_ipp = dcm_rotate.ipp
    
        if dcm_filter_ipp == dcm_rotate_ipp:
            return True
        else:
            return False    
        
        
# Define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class IncorrectNumberOfImages(Error):
    """Raised when there are not 2 images"""
    pass
        
class SameImagePositionPatient(Error):
    """Raised when ipp is the same"""
    pass     


# The following code receives as input the folder containing the images. 
 def main(input_folder):
    
        #Returns a list containing the names of the entries in the directory given by path
        ld = os.listdir(input_folder)
        try:
            
            if len(ld) != 2:
                raise IncorrectNumberOfImages
             
            #The following code is executed if the number of images is exactly 2
            else:
                
                #Create a path for each image
                path1 = os.path.join(input_folder, ld[0])
                path2 = os.path.join(input_folder, ld[1])
                  
                #Create the objects dcm1 and dmc2 of a given class (instantiate the class DcmFilter)
                dcm1 = DcmFilter(path1, 3)
                dcm2 = DcmFilter(path2, 3)
                
                #The following code checks if the objects dcm1 and dcm2 have the same ipp. If this happens, a custom exception appears
                try:
                    if check_ipp(dcm1,dcm2):
                        raise SameImagePositionPatient
                        
                    #The code below is executed if the images do not have the same ipp (path)
                    else: 
                        
                        #Create the attributes original1 and original2 from the objects dcm1 and dcm2.
                        #These attributes store the original pixels as a NumPy array
                        original1 = dcm1.original
                        original2 = dcm2.original
                        
                        #Subtraction operation to obtain the first residue image
                        res1 = original1-original2
                        
                        #Create the attributes filter1 and filter2 from the objects dcm1 and dcm2.
                        #These attributes store the pixels after applying the gaussian filter as a NumPy array
                        filter1 = dcm1.filtered
                        filter2 = dcm2.filtered
                        
                        #Subtraction operation to obtain the second residue image
                        res2 = filter1-filter2
                        
                        #Create the output directory where the residue images will be saved
                        output_dir = os.path.join(input_folder, 'residues')
                        os.mkdir(output_dir)
                        
                        #The subtraction of image pixels leads to some formatting errors that do not allow images to be saved.
                        im1 = Image.fromarray(res1)
                        im1.mode = 'I'
                        im1.point(lambda i:i*(1./256)).convert('L').save(os.path.join(output_dir, 'res1.jpeg'))
                  
                        im2 = Image.fromarray(res2) 
                        im2.mode = 'I'
                        im2.point(lambda i:i*(1./256)).convert('L').save(os.path.join(output_dir, 'res2.jpeg'))
                  
                #If the images have the same ipp (path), a custom exception appears   
                except SameImagePositionPatient:
                     print("The DICOM files appear to be the same. Abborting.")
                     print()
                    
        #If the number of images in the folder is not exactly 2, a custom exception appears
        except IncorrectNumberOfImages:
            print("Incorrect number of images. Aborting.")
            print()

#In order to run the module as if it was a script, we implement the "main" method
if __name__ == '__main__':
    main('images')


    
        
  
     
                
         




