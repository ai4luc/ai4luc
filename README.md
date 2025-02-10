# Artificial Intelligence for Land Use and Land Cover Classification (AI4LUC)

## Overview
`AI4LUC` is a tool designed to assist you with dataset creating:
- Image patch generation 
- Image channels merging
- Reference mask generation (labeled or unlabeled)

The `Utility` module contains these image pre-processing steps, e.g., crop images into patches of 256x256px. `Smart Mask Labeling` is the main module of this version that you can import to generate either labeled or unlabeled reference masks to support supervised deep learning model training. For default it provides a trained model, `CerraNetv3` - a scene classification model - on CerraData-3 dataset. 

## Get start!!

To simply run the source code, do the following steps:

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installer for conda;
2. Create a new environment
    ```
    conda create -n ai4luc
    ```
3. Activate it
    ```
    conda activate ai4luc
    ```


4. Install packs:
    ```
    pip install -r requirements.txt
    ```
5. Alternatively, you can create your env install the environment.yml:     
    ```
    conda env create -f environment.yml
    ```


For users of Apple devices with any version of the M chip, use the [tensorflow-metal](https://developer.apple.com/metal/tensorflow-plugin/) additional GPU usage setting to train models written with TensorFlow package more efficiently and quickly.

6. **Clone** the reposotiry and **download** the dataset, By default the running code will search for the dataset in `/cerradov3/` directory within. Or cloning the repository:
    ```
    git clone https://github.com/ai4luc/AI4LUC.git
    ```

7. If you want to create your own database, consider starting from the first module of the pipeline. Label your dataset by assigning a label to the image patch. Then use CerraNetv3 to learn how to classify your dataset. After the model is trained, use the `.hdf5` file in the python `ai_ContextualClassificatio.py` file inside the `smart_mask_labeling module`.

The specific use instructions for the modules are described in each directory in this repository. 

## Acknowledgments

This research was developed within the [**IDeepS**](https://github.com/vsantjr/IDeepS) project which is supported by the Brazilian LNCC/MCTI via resources of the [SDumont supercomputer](http://sdumont.lncc.br). This research was also supported by the Brazilian agencies CAPES. 

## Reference
MIRANDA, M. S. AI4LUC: pixel-based classification of land use and land cover via deep learning and a cerrado image dataset. version: 2023-04-03. 101 p. IBI: <8JMKD3MGP3W34T/48QQB65>. Dissertação (Mestrado em Computação Aplicada) - Instituto Nacional de Pesquisas Espaciais (INPE), São José dos Campos, 2023. Available in: ...

```
    @MastersThesis{Miranda::PiClLa,
                   author = "Miranda, Mateus de Souza",
                    title = "AI4LUC: pixel-based classification of land use and land cover via 
                             deep learning and a cerrado image dataset",
                   school = "Instituto Nacional de Pesquisas Espaciais (INPE)",
                  address = "S{\~a}o Jos{\'e} dos Campos",
                    month = "2023/03/28",
                 keywords = "classifica{\c{c}}{\~a}o de imagem baseada em pixels, rede neural 
                             convolucional, cerrado, sensoriamento remoto, CBERS-4A, image 
                             pixel-based classification, convolutional neural network, cerrado, 
                             remote sensing, CBERS-4A.",
                committee = "Santiago J{\'u}nior, Valdivino Alexandre de and K{\"o}rting, 
                             Thales Sehn and Shiguemori, Elcio and Escada, Maria Isabel Sobral 
                             and Papa, Jo{\~a}o Paulo",
             englishtitle = "AI4LUC: classifica{\c{c}}{\~a}o baseada em pixels de uso e 
                             cobertura da Terra atrav{\'e}s de aprendizado profundo e um 
                             conjunto de imagens sobre o Cerrado",
                 language = "en",
                    pages = "101",
                      ibi = "8JMKD3MGP3W34T/48QQB65",
                      url = "http://urlib.net/ibi/8JMKD3MGP3W34T/48QQB65",
               targetfile = "Master's dissertation by Mateus de Souza Miranda CAP INPE 
                             Official_com marcas.pdf",
            urlaccessdate = "09 abr. 2023"
    }
```


## Tutorial

1. How to call `CerraNetv3`:

```
from ai4luc.cerranet_v3 import cerranetv3_keras
from from ai4luc.cerranet_v3 import cerranetv3_torch


if __name__ == "__main__":
    # Initialize model with different channel configurations
    rgb_model = cerranetv3_keras.CerranetV3(
        image_size=256,
        num_classes=8,
        channels=3,  # For RGB images
        act_layer='softmax'
    ).build_model()
    
    # Display architectures
    print("RGB Model Summary:")
    rgb_model.summary()
    
    # Torch model
    torch_model = cerranetv3_torch.Cerranetv3(
    num_classes = 8,
    pretrained=False
    )
    
```

 2. Utility: To merge the image channels:

```
from ai4luc.utility import merge_bands
merge_bands(band_indices=[4,3,2], output_dir='new_output', required_bands=6)
```

 3. Utility: To crop the image into patches:
    
```
from ai4luc.utility import GeospatialProcessor


#1 Example usage
config = {
    'input_dir': '../data/render',
    'clip_output_dir': 'images/clip',
    'nodata_dir': 'images/nodata',
    'data_dir': 'images/valid',
    'tile_width': 256,
    'tile_height': 256,
    'nodata_threshold': 98,
    'min_valid_pixels': 0.85,
    'clipping_method': 'translate',
    'output_format': 'GTiff'
}

processor = GeospatialProcessor(config)
processor.process_rasters()

#2 Example usage
custom_config = {
    'input_dir': 'path/to/new/input',
    'clip_output_dir': 'custom/clip/dir',
    'nodata_dir': 'custom/nodata',
    'data_dir': 'custom/valid',
    'tile_width': 512,
    'tile_height': 512,
    'nodata_threshold': 95,
    'min_valid_pixels': 0.9,
    'clipping_method': 'warp',
    'output_format': 'ENVI'
}

custom_processor = GeospatialProcessor(custom_config)
custom_processor.process_rasters()

```
 4. Smart mask labeling

```
from ai4luc.smart_mask_labeling import main

path_input = '../data/images/20200428_209_132_L4_135106.tif'
path_output = '../data/images_patches/'

if __name__ == '__main__':
    main(path_dataset=path_input, filter_mask='bnow_otsu', classify_mask=True, address_to_save=path_output)
```

## Contact 
If you have any questions, please let us know at mateus.miranda@inpe.br
