"""
INSTITUTO NACIONAL DE PESQUISAS ESPACIAIS
COMPUTACAO APLICADA
AUTHOR: MATEUS DE SOUZA MIRANDA, 2022
"""
import os
import glob
import pandas as pd
import earthpy.spatial as es


def merge_bands(
        input_dir='data/raw',
        output_dir='data_preprocessed/composite_images',
        band_indices=[4, 2, 1],
        required_bands=5,
        file_extension='.tif',
        sort_function=sorted,
        naming_band_index=0,
        verbose=True
):
    """
    Process geospatial data from multiple directories and create multi-band composites.

    Parameters:
    input_dir (str): Root directory containing subdirectories with band files
    output_dir (str): Output directory for processed images
    band_indices (list): Indices of bands to composite (NIR, Green, Blue order)
    required_bands (int): Required number of bands per subdirectory
    file_extension (str): Image file extension to process
    sort_function (function): Function to sort band files
    naming_band_index (int): Index of band to use for output naming
    verbose (bool): Show processing progress

    Returns:
    DataFrame: Metadata of processed images
    """

    def validate_inputs():
        if not os.path.exists(input_dir):
            raise ValueError(f"Input directory not found: {input_dir}")
        if max(band_indices) >= required_bands:
            raise ValueError("Band indices exceed available bands count")

    def setup_output():
        os.makedirs(output_dir, exist_ok=True)
        return pd.DataFrame(columns=['Subdirectory', 'Band_Paths', 'Output_File'])

    def process_subdir(subdir, metadata_df):
        try:
            band_files = sort_function(glob.glob(os.path.join(subdir, f'*{file_extension}')))

            if len(band_files) < required_bands:
                if verbose:
                    print(f"Skipping {os.path.basename(subdir)} - insufficient bands")
                return metadata_df

            selected_bands = [band_files[i] for i in band_indices]
            output_name = os.path.basename(band_files[naming_band_index])
            output_path = os.path.join(output_dir, output_name)

            es.stack(selected_bands, out_path=output_path)

            if verbose:
                print(f"Processed: {output_path}")

            return metadata_df.append({
                'Subdirectory': subdir,
                'Band_Paths': selected_bands,
                'Output_File': output_path
            }, ignore_index=True)

        except Exception as e:
            print(f"Error processing {subdir}: {str(e)}")
            return metadata_df

    # Main execution flow
    validate_inputs()
    metadata_df = setup_output()

    subdirs = [d for d in glob.glob(os.path.join(input_dir, '*')) if os.path.isdir(d)]

    for subdir in subdirs:
        metadata_df = process_subdir(subdir, metadata_df)

    metadata_df.to_csv(os.path.join(output_dir, 'processing_metadata.csv'), index=False)
    return metadata_df

# Example usage:
# merge_bands(band_indices=[4,3,2], output_dir='new_output', required_bands=6)