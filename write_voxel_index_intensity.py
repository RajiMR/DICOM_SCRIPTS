import nibabel as nib
import numpy as np
import os 
import pandas as pd
import argparse

def write_intensity_voxel_coords(args):
   
    image_path_list = args.imageFiles
    mask_path = args.mask
    output_path = args.outputFile
    
    """Writes intensity and voxel coordinates to a file for masked voxels."""

    df_comb = pd.DataFrame()
    for image in image_path_list:
        img = nib.load(image)
        mask_img = nib.load(mask_path)
    
        # Get the image and mask data as NumPy arrays
        image_data = img.get_fdata()
        mask_data = mask_img.get_fdata()
    
        # Ensure the image and mask have the same dimensions
        if image_data.shape != mask_data.shape:
            raise ValueError(f"{image} :Image and mask must have the same dimensions")
    
        # Find the voxel indices where the mask is 1
        mask_indices = np.where(mask_data == 1)
    
        # Get the intensities at the mask indices
        intensities = image_data[mask_indices]

        fname = os.path.basename(image)
        df_int = pd.DataFrame({fname : intensities}) 
        df_comb = pd.concat([df_comb, df_int], axis=1)

    df_voxel = pd.DataFrame({'voxel_index' : zip(*mask_indices)})
    df_voxel[['x', 'y', 'z']] = pd.DataFrame(df_voxel['voxel_index'].tolist(), index=df_voxel.index)
    df = pd.concat([df_voxel[['x', 'y', 'z']], df_comb], axis=1)
    #df.columns = ['x', 'y', 'z', 'mpmri_cd', 'mm_cd']
    df.columns = ['x', 'y', 'z', 't1', 't2', 'tc', 'fl', 'ki67', 'cd', 'adc', 'dti', 'hormuth_cd']
    df.to_csv(output_path, index = False)
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--imageFiles', nargs='+', help='List of nifti image filenames')
    parser.add_argument("--mask", help= "your nifti mask file path")
    parser.add_argument("--outputFile", help= "your output csv file")
    args = parser.parse_args()

    write_intensity_voxel_coords(args=args)
    
    ##%run write_voxel_index_intensity.py --imageFiles {t1} {t2} {tc} {fl} {ki67} {cd} --mask {mask} --outputFile {outFile}
