from pprint import pprint
import unittest
from data_structures.location_graph import LocationGraph


def contained_garden(n):
    l = [[0]*n for i in range(n)]
    
    # Inner garden
    if n>4:
        for i in range(n-4):
            for j in range(n-4):
                l[i+2][j+2]=i*(n-4)+j

    # Main wall
    wall_value=(n-4)**2
    for i in range(n):
        l[i][1]=wall_value
        l[i][-2]=wall_value
        l[1][i]=wall_value
        l[-2][i]=wall_value

    # Outer area
    for i in range(n):
        l[i][0]=0
        l[i][-1]=0
        l[0][i]=0
        l[-1][i]=0

    return l


def display(garden):
    for i in garden:
        print(" ".join(str(j).rjust(2, ' ') for j in i))
    print('')



display(contained_garden(4))
display(contained_garden(5))
display(contained_garden(6))
display(contained_garden(7))
display(contained_garden(8))