# important functions: MinimumBoundingBox

from scipy.spatial import ConvexHull
from math import sqrt
import numpy as np
from math import atan2, cos, sin, pi


def smallest_angle_relative_to_cardinal_direction(unit_vector_angle, in_Rad=True):
    # Calculates the smallest angle from the normal vector of any bounding box side to a cardinal direction (ie y, x, -y ,-x)
    if in_Rad:
        divisor = np.pi/2
    else:
        divisor = 90
    angle_1 = np.mod(unit_vector_angle, divisor)
    angle_2 = np.mod(unit_vector_angle, -divisor)
    if abs(angle_1) < abs(angle_2):
        return angle_1
    return angle_2                  
            
    
def unit_vector(pt0, pt1):
    # returns a unit vector that points in the direction of pt0 to pt1
    dis_0_to_1 = sqrt((pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2)
    return (pt1[0] - pt0[0]) / dis_0_to_1, \
           (pt1[1] - pt0[1]) / dis_0_to_1


def orthogonal_vector(vector):
    # from vector returns a orthogonal/perpendicular vector of equal length
    return -1 * vector[1], vector[0]


def bounding_area(index, hull):
    unit_vector_p = unit_vector(hull[index], hull[index+1])
    unit_vector_o = orthogonal_vector(unit_vector_p)

    dis_p = tuple(np.dot(unit_vector_p, pt) for pt in hull)
    dis_o = tuple(np.dot(unit_vector_o, pt) for pt in hull)

    min_p = min(dis_p)
    min_o = min(dis_o)
    len_p = max(dis_p) - min_p
    len_o = max(dis_o) - min_o

    return {'area': len_p * len_o,
            'length_parallel': len_p,
            'length_orthogonal': len_o,
            'rectangle_center': (min_p + len_p / 2, min_o + len_o / 2),
            'unit_vector': unit_vector_p,
            }


def to_xy_coordinates(unit_vector_angle, point):
    # returns converted unit vector coordinates in x, y coordinates
    angle_orthogonal = unit_vector_angle + pi / 2
    return point[0] * cos(unit_vector_angle) + point[1] * cos(angle_orthogonal), \
           point[0] * sin(unit_vector_angle) + point[1] * sin(angle_orthogonal)


def rotate_points(center_of_rotation, angle, points):
    # Requires: center_of_rotation to be a 2d vector. ex: (1.56, -23.4)
    #           angle to be in radians
    #           points to be a list or tuple of points. ex: ((1.56, -23.4), (1.56, -23.4))
    # Effects: rotates a point cloud around the center_of_rotation point by angle
    rot_points = []
    ang = []
    for pt in points:
        diff = tuple([pt[d] - center_of_rotation[d] for d in range(2)])
        diff_angle = atan2(diff[1], diff[0]) + angle
        ang.append(diff_angle)
        diff_length = sqrt(sum([d**2 for d in diff]))
        rot_points.append((center_of_rotation[0] + diff_length * cos(diff_angle),
                           center_of_rotation[1] + diff_length * sin(diff_angle)))

    return rot_points


def rectangle_corners(rectangle):
    # Requires: the output of mon_bounding_rectangle
    # Effects: returns the corner locations of the bounding rectangle
    corner_points = []
    for i1 in (.5, -.5):
        for i2 in (i1, -1 * i1):
            corner_points.append((rectangle['rectangle_center'][0] + i1 * rectangle['length_parallel'],
                            rectangle['rectangle_center'][1] + i2 * rectangle['length_orthogonal']))

    return rotate_points(rectangle['rectangle_center'], rectangle['unit_vector_angle'], corner_points)


# use this function to find the listed properties of the minimum bounding box of a point cloud
def MinimumBoundingBox(points):
    # Requires: points to be a list or tuple of 2D points. ex: ((5, 2), (3, 4), (6, 8))
    #           needs to be more than 2 points
    # Effects:  returns a dictionary that contains:
    #               area: area of the rectangle
    #               length_parallel: length of the side that is parallel to unit_vector
    #               length_orthogonal: length of the side that is orthogonal to unit_vector
    #               rectangle_center: coordinates of the rectangle center
    #                   (use rectangle_corners to get the corner points of the rectangle)
    #               unit_vector: direction of the length_parallel side. RADIANS
    #                   (it's orthogonal vector can be found with the orthogonal_vector function
    #               unit_vector_angle: angle of the unit vector
    #               corner_points: set that contains the corners of the rectangle

    if len(points) <= 2: raise ValueError('More than two points required.')

    hull_ordered = [points[index] for index in ConvexHull(points).vertices]
    hull_ordered.append(hull_ordered[0])
    hull_ordered = tuple(hull_ordered)

    min_rectangle = bounding_area(0, hull_ordered)
    for i in range(1, len(hull_ordered)-1):
        rectangle = bounding_area(i, hull_ordered)
        if rectangle['area'] < min_rectangle['area']:
            min_rectangle = rectangle
            
    # math.atan2 convention is atan2(y,x)
    min_rectangle['unit_vector_angle'] = atan2(min_rectangle['unit_vector'][1], min_rectangle['unit_vector'][0])
    min_rectangle['rectangle_center'] = to_xy_coordinates(min_rectangle['unit_vector_angle'], min_rectangle['rectangle_center'])
    min_rectangle['corner_points'] = set(rectangle_corners(min_rectangle))
    min_rectangle['cardinal_angle_rad'] = smallest_angle_relative_to_cardinal_direction(min_rectangle['unit_vector_angle'], True)
    min_rectangle['cardinal_angle_deg'] = np.rad2deg(min_rectangle['cardinal_angle_rad'])

    return min_rectangle
