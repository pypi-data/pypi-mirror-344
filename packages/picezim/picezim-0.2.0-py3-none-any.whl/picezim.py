import math


def calculate_new_diameter(cost):
    # Area of the original 20 cm diameter pizza
    d_20 = 20  # diameter of the original pizza
    area_20 = math.pi * (d_20 / 2) ** 2

    # Calculate the new area based on cost
    area_new = area_20 * (cost / 3)

    # Calculate the new diameter from the new area
    d_new = 2 * math.sqrt(area_new / math.pi)

    return d_new, area_new
