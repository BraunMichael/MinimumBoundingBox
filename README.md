# MinimumBoundingBox
Finds the minimum bounding box from a point cloud.  

[![Build Status](https://travis-ci.org/BebeSparkelSparkel/MinimumBoundingBox.svg?branch=master)](https://travis-ci.org/BebeSparkelSparkel/MinimumBoundingBox)

![](https://github.com/BraunMichael/MinimumBoundingBox/blob/master/visual.png?raw=true)

### Example
```python
from MinimumBoundingBox import MinimumBoundingBox

points = ( (1,2), (5,4), (-1,-3) )
bounding_box = MinimumBoundingBox(points)  # returns namedtuple

bounding_box.area  # 16
bounding_box.rectangle_center  # (1.3411764705882352, 1.0647058823529414)
bounding_box.corner_points  # {(5, 4), (-1, -3), (-2.32, -1.87), (3.68, 5.13)}
```

### Install
```shell
pip install git+git://github.com/BraunMichael/MinimumBoundingBox.git@master
pip3 install git+git://github.com/BraunMichael/MinimumBoundingBox.git@master
pip3.5 install git+git://github.com/BraunMichael/MinimumBoundingBox.git@master
```

**MinimumBoundingBox**(points)  
Returns the properties of the bounding box in a dict
* **area**: area of the rectangle  
* length_parallel: length of the side that is parallel to unit_vector  
* length_orthogonal: length of the side that is orthogonal to unit_vector  
* **rectangle_center**: coordinates of the rectangle center  
  * use rectangle_corners to get the corner points of the rectangle
* unit_vector: direction of the length_parallel side. RADIANS  
  * it's orthogonal vector can be found with the orthogonal_vector function
* unit_vector_angle: angle of the unit vector  
* **corner_points**: set that contains the corners of the rectangle
