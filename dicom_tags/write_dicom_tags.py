##Extract dicom tags and values - Save to CSV file
import pydicom
import csv, os
import pandas as pd
import argparse

def get_dicom_tags_to_csv(args):

    dicom_folder = args.dicomFolderpath
    csv_filepath = args.outputFilepath
    
    """Extract tags from a DICOM file and save them to a CSV file."""
    filename = os.listdir(dicom_folder)[0]
    file_path = os.path.join(dicom_folder, filename)
    df = pd.DataFrame()
    
    with pydicom.dcmread(file_path) as ds:
       
        for elem in ds:
            #print(elem)
            tag = str(elem.tag)
            name = elem.name
            vr = elem.VR
            value = str(elem.value)

            file_content = [tag, name, vr, value]
            para = pd.DataFrame(file_content).T 
            df = pd.concat([df, para], ignore_index=True)
    
    foldername = ds.PatientID  
    filename = ds.SeriesDescription
    
    os.makedirs(os.path.join(csv_filepath, foldername), exist_ok=True)
    outFile = os.path.join(csv_filepath, foldername, filename + '.csv')
    
    df.columns=['Tag', 'Name', 'VR', 'Value']
    df.to_csv(outFile, index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dicomFolderpath", help="Enter path to dicom folder")
    parser.add_argument("--outputFilepath", help="Enter output CSV filepath")
    args = parser.parse_args()

    get_dicom_tags_to_csv(args=args)