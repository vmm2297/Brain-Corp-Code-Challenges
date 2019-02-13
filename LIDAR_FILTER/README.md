# LIDAR FILTER

## Description

The challenge is to write filters to reduce noise in the data coming from a [LIDAR](https://en.wikipedia.org/wiki/Lidar) sensor attached to a robot. The LIDAR generates scans at a certain rate. Each scan is an array of length N of float values representing distance measures. N is typically in a range of ~[200, 1000] measurements, and it is fixed. Measured distances are typically in a range of [0.03, 50] meters. Each time a scan is received, it will be passed on to the filters. Each filter object has an **update** method, that takes a length-N array of ranges and returns a filtered length-N array of ranges. My implementation uses [Numpy](http://www.numpy.org/) on [Python 2.7](https://www.python.org/download/releases/2.7/).

## Range Filter

The **range filter** crops all the values that are below range\_min (resp. above range\_max), and replaces them with range\_min value (resp. range\_max).

## Temporal Median Filter

DESCRIPTION HERE