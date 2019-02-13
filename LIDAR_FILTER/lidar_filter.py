import numpy as np

class RangeFilter(object):

	def __init__(self, range_min, range_max):
		self.range_min = range_min # min range value
		self.range_max = range_max # max range value

	def update(self, lidar_data):
		filter_data = np.array(lidar_data)
		filter_data[filter_data<self.range_min] = self.range_min
		filter_data[filter_data>self.range_max] = self.range_max
		return filter_data

class MedianFilter(object):

	def __init__(self, D, N):
		self.i = 0 # counter
		self.D = D # first D scans
		self.filter_data = np.zeros([D+1,N]) # initializa D+1 x N matrix

	def update(self, lidar_data):
		# FIFO
		self.filter_data[1:,:] = self.filter_data[:-1,:]
		self.filter_data[0,:] = np.array(lidar_data)
		# conditional until counter == D
		if (self.i < self.D):
			self.i = self.i + 1
			return np.median(filter_data[:self.i,:], axis=0)
		else:
			return np.median(filter_data, axis=0)