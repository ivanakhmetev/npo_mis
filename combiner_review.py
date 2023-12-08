from typing import List
from raster_design import raster_design #spatial_reader / spatial_raster? 
import rasterio

class combiner(): #наследование от класса для чтения нелогично

    def __init__(self, files: List[str]): #класс делает сопоставление между индексами файлов, значит должен получать файлы

        def init_rasters(files):
            return list(map(raster_design, files))
        
        def init_height_meters(raster: raster_design):
            return raster.get_height_meters()
        
        def init_width_meters(raster: raster_design):
            return raster.get_width_meters()
        
        def init_width_pixels(raster: raster_design):
            return raster.get_width_pixels()
        
        def init_height_pixels(raster: raster_design):
            return raster.get_height_pixels()  

        self.rasters = init_rasters(files) #в инит только инициализация файлов для работы, остальные вычисления - по запросу
        self.height_meters = init_height_meters(self.rasters[0]) #избавились от глобальной переменной
        self.width_meters = init_width_meters(self.rasters[0]) #учли возможность не квадратных блоков
        self.height_pixels = init_height_pixels(self.rasters[0]) # надо ли в __init__? вместо def get_matrix_size_in_pxl(self):
        self.width_pixels = init_width_pixels(self.rasters[0]) 

    def get_positioning(self): #улучшено название функции - должно быть глагол-действие
        '''TODO проверить для полушарий'''
        left_bounds = self.get_left_bounds()
        top_bounds = self.get_top_bounds()
        leftmost = min(left_bounds) #улучшено название переменной
        uppermost = max(top_bounds)        
        positioning = {} #улучшено название, переменная инициализируется наиболее близко к области применения, а не в начале
        for raster in self.rasters:#[:2]:
            key_index = raster.file.get_image()
            '''TODO проверить col-width height - row'''
            # print(raster.get_left_bound())
            row_index = int(abs(uppermost - raster.get_top_bound()) / self.height_meters) #с abs более понятно кажется, но считается неверно 
            col_index = int(abs(leftmost - raster.get_left_bound()) / self.width_meters)  
            positioning[key_index] = (row_index, col_index)
        return positioning
    
    def get_combined_transform(self):
        '''TODO проверить корректность для разных полушарий'''
        left_bounds = self.get_left_bounds()
        top_bounds = self.get_top_bounds()
        right_bounds = self.get_right_bounds()
        bottom_bounds = self.get_bottom_bounds()

        leftmost = min(left_bounds)
        rightmost = max(right_bounds)
        topmost = max(top_bounds) #было north = min(top_bounds)
        bottommost = min(bottom_bounds) #было south = max(bottom_bounds)
        
        combined_width_pixels = self.width_pixels * self.get_num_cols_in_positioning() # высота и ширина считалась для одной картинки
        combined_height_pixels = self.height_pixels * self.get_num_rows_in_positioning()   
        return rasterio.transform.from_bounds(leftmost, bottommost, rightmost, topmost, combined_width_pixels, combined_height_pixels)
    
    def get_num_cols_in_positioning(self): #разделили функцию на две более простые
        left_bounds = self.get_left_bounds()
        leftmost = min(left_bounds)
        rightmost = max(left_bounds)
        return int(abs(leftmost - rightmost) / self.width_meters)
    
    def get_num_rows_in_positioning(self):
        top_bounds = self.get_top_bounds()
        topmost = max(top_bounds)
        bottommost = min(top_bounds)
        return int(abs(topmost - bottommost) / self.height_meters)
    
    def has_gaps(self): #улучшен синтаксис
        positioning_size = self.get_num_cols_in_positioning() * self.get_num_rows_in_positioning()
        return bool(len(self.rasters) != positioning_size) 
    
    def get_left_bounds(self): #2 раза повторяется вызов - повод вынести код в отдельную функцию
        #долго работает для x32
        return list(map(lambda x: x.get_left_bound(), self.rasters))
    
    def get_top_bounds(self):
        return list(map(lambda x: x.get_top_bound(), self.rasters))
    
    def get_right_bounds(self):
        return list(map(lambda x: x.get_right_bound(), self.rasters))
    
    def get_bottom_bounds(self):
        return list(map(lambda x: x.get_bottom_bound(), self.rasters))

if __name__ == '__main__':
    PATH = '/home/iakhmetev/datasets/sen12ms_learning/train/ROIs2017_winter_s2/s2_119/*'
    # PATH = '/home/iakhmetev/datasets/8/*'
    from glob import glob
    FILES = glob(PATH)
    # print(FILES)
    a = combiner(FILES)
    print(a.height_meters)
    print(a.width_meters)
    print(a.height_pixels)
    print(a.width_pixels)
    print(a.get_positioning())
    # print(a.get_num_cols_in_positioning())
    # print(a.get_num_rows_in_positioning())
    # print(a.has_gaps())
    # print(a.get_combined_transform())

    

