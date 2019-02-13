import numpy as np

class RangeFilter(object):
	def __init__(self, range_min, range_max):
		self.range_min = range_min
		self.range_max = range_max

	def update(self, lidar_data):
		filter_data = np.array(lidar_data)
		filter_data[filter_data<self.range_min] = self.range_min
		filter_data[filter_data>self.range_max] = self.range_max
		return filter_data