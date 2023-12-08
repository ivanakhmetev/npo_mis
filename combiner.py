from file_design import file_design
from raster_design import raster_design
from scene_design import scene_design
import selector_e
import rasterio


LEN_BOUND = 1280
LEN_ONE_PIC_PXL = 256

class combiner(raster_design):

    def __init__(self, rasters: list):
        self.rasters = rasters
        self.has_gap = self.gap_checker()


    def positioning(self):
        matrix = {}
        left_bounds = list(map(lambda x: raster_design(x).get_left_bound(), self.rasters))
        top_bounds = list(map(lambda x: raster_design(x).get_top_bound(), self.rasters))
        lmin = min(left_bounds)
        tmax = max(top_bounds)
        for raster in self.rasters:
            matrix[raster.get_image()] = (int((tmax - raster_design(raster).get_top_bound()) / LEN_BOUND), int((raster_design(raster).get_left_bound() - lmin)/ LEN_BOUND))
        return matrix


    def get_sparse_matrix_size(self):
        left_bounds = list(map(lambda x: raster_design(x).get_left_bound(), self.rasters))
        top_bounds = list(map(lambda x: raster_design(x).get_top_bound(), self.rasters))
        lmin = min(left_bounds)
        lmax = max(left_bounds)
        tmin = min(top_bounds)
        tmax = max(top_bounds)
        dim = (int((tmax - tmin)/LEN_BOUND) + 1, int((lmax - lmin)/LEN_BOUND) + 1)
        return dim


    def get_matrix_size_in_pxl(self):
        w = self.get_sparse_matrix_size()[0] * LEN_ONE_PIC_PXL
        h = self.get_sparse_matrix_size()[1] * LEN_ONE_PIC_PXL
        return (w, h)


    def gap_checker(self):
        area = self.get_sparse_matrix_size()[0] * self.get_sparse_matrix_size()[1]
        if len(self.rasters) == area:
            return False
        else:
            return True

    # def combine_np(self):

    def get_new_transform(self):
        left_bounds = list(map(lambda x: raster_design(x).get_left_bound(), self.rasters))
        top_bounds = list(map(lambda x: raster_design(x).get_top_bound(), self.rasters))
        right_bounds = list(map(lambda x: raster_design(x).get_right_bound(), self.rasters))
        bottom_bounds = list(map(lambda x: raster_design(x).get_bottom_bound(), self.rasters))
        west = min(left_bounds)
        east = max(right_bounds)
        north = min(top_bounds)
        south = max(bottom_bounds)
        '''проверить корректность для разных полушарий'''
        width = self.get_matrix_size_in_pxl()[0]
        height = self.get_matrix_size_in_pxl()[1]
        print(west, south, east, north, width, height)
        return rasterio.transform.from_bounds(west, south, east, north, width, height)





