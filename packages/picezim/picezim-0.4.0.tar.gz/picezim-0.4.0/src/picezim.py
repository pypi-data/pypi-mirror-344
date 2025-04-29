import math


def calculate_new_diameter(current_diameter, current_cost, new_cost):
    # Area of the original 20 cm diameter pizza
    area_20 = math.pi * (current_diameter / 2) ** 2

    # Calculate the new area based on cost
    area_new = area_20 * (new_cost / current_cost)

    # Calculate the new diameter from the new area
    d_new = 2 * math.sqrt(area_new / math.pi)

    return d_new, area_new
