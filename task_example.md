Есть класс который используется в увеличении изображений датасета с сохранением геопривязки
class combiner():
'''combine npblock and geodata'''
	def __init__(self, rasters: list):

для него реализовать: 
1. процедуру (последовательность функций) positioning, выявляющую соотнесение индекса p* в имени файла (rasters[k].abs) и пары индексов (i, j) обозначающих положение файла, соответствующего индексу относительно других на прямоугольной / квадратной матрице.
Пример: p30, p31, p32 → (30, (0, 0)), (31 (0, 1)) , (32, (0, 2)). # структура может быть другая.

Идея реализации: сортировка списка [index, (bound_1, bound_2 …?)] , затем проверка — идут ли  bound_1, bound_2 … по порядку или индекс пропущен. Может быть другая. Хорошая процедура избавит от использования попарных проверок is_vertival_heighbours.

Идея 2. Найти ширину и последовательно увеличивать индексы. 

2. вычисление булевого параметра self.has_gap — True, если есть хотя бы один nan — блок, т. е. недостающий индекс.

3. вычисление размера высоты и ширины итоговой матрицы в пикселях (может быть не квадтратной).

4. предложить способ определения нового индекса p* - отказываемся от суффикса _seg_ (при разделении) в имени файла (потому что тогда надо вводить суффикс и для объединения), т.е. изменем индекс изображения.  Класс только связывает npblock и geodata, соответственно вызывающая функция отвечает за индекс. 

5. вычисление параметра transform матрицы объединения.

6* записать датасет с изображением размера 1024*1024 пикселя без пересечений. Для чего решить задачу поиска нового индекса, объединяющего исходные, с сохранением логики, т. е. индексы идут по порядку слева направо. 



Есть класс который используется в уменьшении изображений датасета с сохранением геопривязки

class separator():
'''separate file to num_npblocks and geodata'''
	def __init__(self, file: file_design, num_npblocks: int):

для него реализовать:

0 (связано с 3.). проверку корректности аргумента num_npblocks — можно ли разделить на равные квадраты.  (могут быть нечетные длины этих квадратов)
1. процедуру get_np((i, j))  возвращающую матрицу значений сегмента, i * j <= num_npblocks, i — row, j — column.
2. процедуру get_transform((i, j)) возвращающую матрицу rasterio.transform.Affine значений сегмента.
3. вычисление размера матрицы сегмента в пикселях (только квадратная)






Примеры плохого кода, делающие преобразование transform 

def get_segmented_transform(transform: affine.Affine, output_image_edge: int, slice_number: int ):
    segments_in_row = 128 / output_image_edge
    transform_as_ndarray = np.array(transform)
    t = transform_as_ndarray
    x_in_row = int(slice_number % segments_in_row)
    y_in_col = int(slice_number / segments_in_row)
    x_position = t[2] + output_image_edge * t[0] * x_in_row
    y_position = t[5] + output_image_edge * t[4] * y_in_col
    return rasterio.transform.Affine(t[0] , t[1], x_position, t[3], t[4], y_position)

def get_scaled_transform(transform: affine.Affine, output_image_edge: int):
    scale_factor = 128 / output_image_edge
    transform_as_ndarray = np.array(transform)
    t = transform_as_ndarray
    return rasterio.transform.Affine(t[0] * scale_factor, t[1], t[2], t[3], t[4] * scale_factor, t[5])
