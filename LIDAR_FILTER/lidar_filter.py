import numpy as np

class RangeFilter(object):
	"""
	A class used to represent a range filter

	The range filter crops all the values that are below
	range_min (resp. above range_max), and replaces them
	with range_min value (resp. range_max).

	Attributes
	----------
	range_min : float, int
		The desired minimum range value
	range_max : float, int
		The desired maximum range value

	Methods
	-------
	update(lidar_data)
		Updates incoming LIDAR data through a range filter
	"""

	def __init__(self, range_min, range_max):
		"""
		Parameters
		----------
		range_min : float, int
			The desired minimum range value
		range_max : float, int
			The desired maximum range value
		"""

		self.range_min = range_min
		self.range_max = range_max

	def update(self, lidar_data):
		"""Updates incoming LIDAR data through a range filter

		Parameters
		----------
		lidar_data : list, ndarray
			Array of N distance measures

		Returns
		-------
		ndarray
			Array of N filtered distance measures
		"""

		filter_data = np.array(lidar_data)
		filter_data[filter_data<self.range_min] = self.range_min
		filter_data[filter_data>self.range_max] = self.range_max
		return filter_data

class MedianFilter(object):
	"""
	A class used to represent a temporal median filter

	The temporal median filter returns the median of the
	current and the previous D scans:

	yi(t) = median( xi(t) , xi(t-1) , ... , xi(t-D) )

	where x and y are input and output length-N scans and i
	ranges from 0 to N-1. The number of previous scans D is
	a parameter that is given when creating a new temporal
	median filter. The update method receives a single scan
	and returns a length-N array depending on the values of
	the previous scans. For the first D scans, the filter
	returns the median of all the scans so far.
	
	Attributes
	----------
	D : int
		Number of previous scans to account for
	N : int
		Length of incoming LIDAR data array

	Methods
	-------
	update(lidar_data)
		Updates incoming LIDAR data through a temporal median filter
	"""

	def __init__(self, D, N):
		"""
		Parameters
		----------
		D : int
			Number of previous scans to account for
		N : int
			Length of incoming LIDAR data array
		"""

		self.D = D
		# global counter to reach i == D previous scans
		self.i = 0
		# initialize "empty" (D+1)x(N) matrix for FIFO
		self.filter_data = np.zeros([D+1,N])

	def update(self, lidar_data):
		"""Updates incoming LIDAR data through a temporal median filter

		Parameters
		----------
		lidar_data : list, ndarray
			Array of N distance measures

		Returns
		-------
		ndarray
			Array of N filtered distance measures
		"""

		# FIFO data processing
		self.filter_data[1:,:] = self.filter_data[:-1,:]
		self.filter_data[0,:] = np.array(lidar_data)
		# conditial until i == D
		if (self.i < self.D):
			self.i = self.i + 1
			return np.median(self.filter_data[:self.i,:], axis=0)
		else:
			return np.median(self.filter_data, axis=0)