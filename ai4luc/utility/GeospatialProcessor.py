"""
INSTITUTO NACIONAL DE PESQUISAS ESPACIAIS
COMPUTACAO APLICADA

CODE: GEOSPATIAL DATA PROCESSOR
AUTHOR: MATEUS DE SOUZA MIRANDA, 2022
REFACTORED: 2023
"""

import os
import glob
import shutil
import numpy as np
from osgeo import gdal


class GeospatialProcessor:
    def __init__(self, config):
        self.config = config
        self.validate_config()
        self.create_directories()

    def validate_config(self):
        required_keys = ['input_dir', 'clip_output_dir', 'nodata_dir', 'data_dir']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

    def create_directories(self):
        os.makedirs(self.config['clip_output_dir'], exist_ok=True)
        os.makedirs(self.config['nodata_dir'], exist_ok=True)
        os.makedirs(self.config['data_dir'], exist_ok=True)

    def process_rasters(self):
        self.clip_count = 0
        self.nodata_count = 0
        self.data_count = 0

        for raster_path in glob.glob(os.path.join(self.config['input_dir'], '*.tif')):
            try:
                output_subdir = self.process_single_raster(raster_path)
                self.filter_nodata(output_subdir)
                self.clip_count += 1
            except Exception as e:
                print(f"Error processing {raster_path}: {str(e)}")

        print(f"\nProcessing complete!\n"
              f"Total rasters processed: {self.clip_count}\n"
              f"Valid tiles: {self.data_count}\n"
              f"NoData tiles: {self.nodata_count}")

    def process_single_raster(self, raster_path):
        with gdal.Open(raster_path) as dataset:
            geotransform = dataset.GetGeoTransform()
            x_size = dataset.RasterXSize
            y_size = dataset.RasterYSize

            tile_width = self.config.get('tile_width', 256)
            tile_height = self.config.get('tile_height', 256)

            x_steps, y_steps = self.calculate_tile_grid(
                geotransform, x_size, y_size, tile_width, tile_height
            )

            output_subdir = self.create_output_subdir(raster_path)
            self.generate_tiles(dataset, geotransform, x_steps, y_steps, output_subdir)

        return output_subdir

    def calculate_tile_grid(self, geotransform, x_size, y_size, tile_w, tile_h):
        x_res = geotransform[1]
        y_res = abs(geotransform[5])

        cols = int(np.ceil(x_size / tile_w))
        rows = int(np.ceil(y_size / tile_h))

        x_steps = [geotransform[0] + i * tile_w * x_res for i in range(cols + 1)]
        y_steps = [geotransform[3] - i * tile_h * y_res for i in range(rows + 1)]

        return x_steps, y_steps

    def create_output_subdir(self, raster_path):
        basename = os.path.basename(raster_path).split('.')[0]
        output_subdir = os.path.join(self.config['clip_output_dir'], f"{basename}_clipped")
        os.makedirs(output_subdir, exist_ok=True)
        return output_subdir

    def generate_tiles(self, dataset, geotransform, x_steps, y_steps, output_dir):
        method = self.config.get('clipping_method', 'translate')
        driver = gdal.GetDriverByName(self.config.get('output_format', 'GTiff'))

        for i in range(len(x_steps) - 1):
            for j in range(len(y_steps) - 1):
                x_min = x_steps[i]
                x_max = x_steps[i + 1]
                y_max = y_steps[j]
                y_min = y_steps[j + 1]

                output_path = os.path.join(
                    output_dir,
                    f"{os.path.basename(output_dir)}_{i}_{j}.tif"
                )

                if method.lower() == 'warp':
                    gdal.Warp(output_path, dataset,
                              outputBounds=(x_min, y_min, x_max, y_max),
                              dstNodata=self.config.get('nodata_value'))
                else:
                    gdal.Translate(output_path, dataset,
                                   projWin=(x_min, y_max, x_max, y_min),
                                   xRes=geotransform[1],
                                   yRes=-abs(geotransform[5]))

    def filter_nodata(self, input_dir):
        threshold = self.config.get('nodata_threshold', 98)
        min_pixels = self.config.get('min_valid_pixels', 0.8)

        for tile_path in glob.glob(os.path.join(input_dir, '*.tif')):
            with gdal.Open(tile_path) as ds:
                array = ds.ReadAsArray()
                valid_pixels = np.sum(array > threshold)
                total_pixels = array.size

                if (valid_pixels / total_pixels) < min_pixels:
                    dest_dir = self.config['nodata_dir']
                    self.nodata_count += 1
                else:
                    dest_dir = self.config['data_dir']
                    self.data_count += 1

                shutil.move(tile_path, os.path.join(dest_dir, os.path.basename(tile_path)))


""" 
Example:
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

"""
