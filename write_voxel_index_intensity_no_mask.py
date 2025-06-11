import nibabel as nib
import numpy as np
import os 
import pandas as pd
import argparse

def strip_ext(filename):
    if filename.endswith(".nii.gz"):
        return filename[:-7]
    elif filename.endswith(".nii"):
        return filename[:-4]
    else:
        return filename
        
def write_intensity_voxel_coords(args):
   
    image_path_list = args.imageFiles
    output_path = args.outputFile
    
    df_comb = pd.DataFrame()

    """
    Extracts voxel IDs and intensities from a NIfTI image and saves them to a text file.

    Args:
        file_path (str): Path to the NIfTI image file (.nii.gz).
        output_file (str): Path to the output text file.
    """

    for image in image_path_list:
        img = nib.load(image)
        data = img.get_fdata()

        voxx = []
        voxy = []
        voxz = []
        inten = []
        # Iterate through the 3D array indices and values
        for x in range(data.shape[0]):
            for y in range(data.shape[1]):
                for z in range(data.shape[2]):
                    voxel_x = x
                    voxel_y = y
                    voxel_z = z
                    intensity = data[x, y, z]
                    voxx.append(voxel_x)
                    voxy.append(voxel_y)
                    voxz.append(voxel_z)
                    inten.append(intensity)
        
        fname1 = os.path.basename(image)
        fname2 = strip_ext(fname1)
        print(fname2)

        df_int = pd.DataFrame({fname2 : inten}) 
        df_comb = pd.concat([df_comb, df_int], axis=1)
    
    df_x = pd.DataFrame({'x' : voxx}) 
    df_y = pd.DataFrame({'y' : voxy}) 
    df_z = pd.DataFrame({'z' : voxz}) 

    df = pd.concat([df_x, df_y, df_z, df_comb], axis=1)
    df.to_csv(output_path, index = False)
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--imageFiles', nargs='+', help='List of nifti image filenames')
    parser.add_argument("--mask", help= "your nifti mask file path")
    parser.add_argument("--outputFile", help= "your output csv file")
    args = parser.parse_args()

    write_intensity_voxel_coords(args=args)
