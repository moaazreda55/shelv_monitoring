import numpy as np


class shelv_data:
    
    def _init_(self,box):
        box_int = box.numpy().astype(np.int32)
        self.p1 = box_int[0]
        self.p2 = box_int[1]
        self.p3 = box_int[2]
        self.p4 = box_int[3]


class product_data:
    def __init__(self, box):
        self.points = box.numpy()  # Store all 4 corners of OBB
        self.p1 = [self.points[0], self.points[1]]  # First point
        self.p2 = [self.points[2], self.points[3]] 
        