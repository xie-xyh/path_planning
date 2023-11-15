from Ship import Ship
from calCPA import calCPA
import numpy as np
listA = [123456789, 120.5, 25.6, 45.0, 10.0, 90.0, 50.0, 15.0, 123]
listB = [987654321, 121.0, 25.8, 120.0, 8.0, 120.0, 40.0, 12.0, 321]

shipA = Ship(listA)
shipB = Ship(listB)

cpa = calCPA(shipA,shipB)

print(cpa.getCPA())
