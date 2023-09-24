import math

import click
from math import sqrt, acos, pi, degrees

def is_move(command):
    """Checks if input G-code line is a linear move (rapid or with feed rate) command.
    @:param line: The G-code input line
    @:return True if the line is a linear move, False if not."""
    if command:
        return command.find('G00') > -1 or command.find('G01') > -1
    return False

def is_arc(command):
    """Checks if input G-code line is a circular arc (clockwise or counter-clockwise) command.
    @:param command: The G-code input line
    @:return True if the line is an arc move, False if not."""
    if command:
        return (command.find('G02') > -1) or (command.find('G03') > -1)
    return False

def parse_coordinates(line):
    """Reads a move command and converts it into a float value set
    @:param line: a move command
    @:return a float value set."""
    values = line.split(' ')
    coordinate = [None, None, None, None, None]
    for value in values:
        if value.find('X') > -1:
            coordinate[0] = float(value.strip('X '))
        if value.find('Y') > -1:
            coordinate[1] = float(value.strip('Y '))
        if value.find('Z') > -1:
            coordinate[2] = float(value.strip('Z '))
        if value.find('I') > -1:
            coordinate[3] = float(value.strip('I '))
        if value.find('J') > -1:
            coordinate[4] = float(value.strip('J '))
    return coordinate


def get_max_by_column(data, column_index):
    # column_index - 1 is used to 'hide' the fact lists' indexes are zero-based from the caller
    return max(data, key=lambda x: x[column_index - 1])


def get_min_by_column(data, column_index):
    return min(data, key=lambda x: x[column_index - 1])


def get_arc_degrees(coordinates, arc_center, radius):
    if radius <= 0:
        return 0
    # cos = dx / radius
    cos = round((coordinates[0] - arc_center[0]) / radius, 3)
    rad = acos(cos)
    if coordinates[1] < 0:
        #  negative y, add 180°
        rad += pi
    return degrees(rad)

def fill_coordinates(coordinates, previous_coordinates):
    for i in range(0, 3):
        if coordinates[i] is None:
            coordinates[i] = previous_coordinates[i]
    return coordinates

def handle_linear_move(line, previous_coordinates):
    coordinates =  fill_coordinates(parse_coordinates(line), previous_coordinates)
    return [coordinates[0], coordinates[1], coordinates[2]]

def handle_arc_move(line, previous_coordinates):
    coordinates = parse_coordinates(line)
    coordinates = fill_coordinates(coordinates, previous_coordinates)
    radius = sqrt(coordinates[3] ** 2 + coordinates[4] ** 2)
    arc_center = (previous_coordinates[0] + coordinates[3], previous_coordinates[1] + coordinates[4])

    if line.find('G02') > -1:
        arc_start = get_arc_degrees(coordinates, arc_center, radius)
        arc_end = get_arc_degrees(previous_coordinates, arc_center, radius)
    elif line.find('G03') > -1:
        arc_start = get_arc_degrees(previous_coordinates, arc_center, radius)
        arc_end = get_arc_degrees(coordinates, arc_center, radius)

    else:
        return [] #  command does not fit move pattern and will not count.

    # min/max calculations needed later on
    xyz = [coordinates[0], coordinates[1], coordinates[2]]
    x_center = previous_coordinates[0] + coordinates[3]
    y_center = previous_coordinates[1] + coordinates[4]
    x_plus_radius = [x_center + radius, y_center, coordinates[2]]
    y_plus_radius = [x_center, y_center + radius, coordinates[2]]
    x_minus_radius = [x_center - radius, y_center, coordinates[2]]
    y_minus_radius = [x_center, y_center - radius, coordinates[2]]
    extremevalue_order = [0, y_plus_radius, x_minus_radius, y_minus_radius, x_plus_radius]

    arcdiff = arc_end - arc_start
    if arcdiff < 0:
        # crossing the 0° line (x-axis)
        arc_end += 360

    #print(arc_start)
    #print(arc_end)

    result = []
    for crossing_angle in range (90, 361, 90):
        if crossing_angle in range(int(arc_start), int(arc_end)):
            result.append(extremevalue_order[int(crossing_angle/90)])

    result.append(xyz)
    return result


@click.command()
@click.argument(
    "file",
    type=click.File(mode="r"),
)
@click.option("--name", prompt="enter name", help="name of the user")
def hello(file, name):
    click.echo(f"Hello {name}!")

    data = []
    with file as f:
        lines = f.readlines()

        previous_coordinates = [0, 0, 0]
        for line in lines:
            line = line.strip()
            if is_move(line):
                data.append(handle_linear_move(line, previous_coordinates))
            elif is_arc(line):
                extreme_values = handle_arc_move(line, previous_coordinates)
                if lines:
                    data.extend(extreme_values)
            if data:
                previous_coordinates = data[-1]

    print(get_max_by_column(data, 0))
    print(get_min_by_column(data, 0))
    print(get_max_by_column(data, 1))
    print(get_min_by_column(data, 1))
    print(get_min_by_column(data, 2))

if __name__ == "__main__":
    hello()
