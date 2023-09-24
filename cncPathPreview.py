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
    """@:param data: the input list, column_index: the column to find the max for
    @:return the line that contains the maximum value of a given column"""
    return max(data, key=lambda x: x[column_index])

def get_min_by_column(data, column_index):
    """@:param data: the input list, column_index: the column to find the min for
    @:return the line that contains the minimum value of a given column"""
    return min(data, key=lambda x: x[column_index])

def get_arc_degrees(coordinates, arc_center, radius):
    """@:param coordinates: the input vector, arc_center: coordinates, radius: arc radius
    @:return arc's length in degrees"""
    if radius <= 0:
        return 0
    # cos = dx / radius
    cos = (coordinates[0] - arc_center[0]) / radius
    rad = acos(cos)
    if (coordinates[1] - arc_center[1]) < 0:
        #  negative y, count from 360° backwards
        rad = 2*pi - rad
    return round(degrees(rad), 0)

def fill_coordinates(coordinates, previous_coordinates):
    """helper that removes 'None' values from a line by filling with last known coordinate values
    @:param coordinates: the current target vector, previous_coordinates: valid target vector from the past
    @:return the filled coordinate vector"""
    for i in range(0, 3):
        if coordinates[i] is None:
            coordinates[i] = previous_coordinates[i]
    return coordinates

def handle_linear_move(line, previous_coordinates):
    """handles a linear move command by parsing into floats, filling in 'None values'.
    @:param line: an input command, previous_coordinates: a valid target coordinate from the past
    @:return a valid coordinate"""
    coordinates =  fill_coordinates(parse_coordinates(line), previous_coordinates)
    return [coordinates[0], coordinates[1], coordinates[2]]

def handle_arc_move(line, previous_coordinates):
    """handles an arc move command by parsing into floats, filling in 'None values', finding out movement direction,
    arc radius, span, and position. It then finds the arc's extreme values and returns them.
    @:param line: an input command, previous_coordinates: a valid target coordinate from the past
    @:return one or multiple valid coordinates depending on arc length and position"""
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
    z_safety = 25

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

    target_filename = 'PathPreview_' + file.name

    with open(target_filename, 'w') as f:
        f.write(getfileheader(target_filename))
        f.write(get_info_z_min(get_min_by_column(data, 2)[2]))
        f.write(get_gcode_rapidmove([0, 0, z_safety]))

        y = get_min_by_column(data, 1)
        y[2] = z_safety
        f.write(get_info_coordinate('Y', y))
        x = get_min_by_column(data, 0)
        x[2] = z_safety
        f.write(get_info_coordinate('X', x))
        y = get_max_by_column(data, 1)
        y[2] = z_safety
        f.write(get_info_coordinate('Y', y))
        x = get_max_by_column(data, 0)
        x[2] = z_safety
        f.write(get_info_coordinate('X', x))

        f.write('M30')
        f.close()

    print(get_max_by_column(data, 0))
    print(get_min_by_column(data, 0))
    print(get_max_by_column(data, 1))
    print(get_min_by_column(data, 1))
    print(get_min_by_column(data, 2))

def getfileheader(targetfilename):
    return ('(PathPreview by Schallbert, 2023)\n'
            '(File output is supplied without liability.)\n'
            '(Output paths must be checked for correctness before usage.)\n\n'
            '(Project: ' + targetfilename + ')\n\n'
            'G90\n\n')

def get_info_coordinate(axis, coordinate):
    value = 0
    if axis == 'X':
        value = coordinate[0]
    elif axis == 'Y':
        value = coordinate[1]
    return ('DLGMSG "PathPreview" "Go to ' + axis + ': ' + str(round(value, 3)) + '?"\n'
          'IF [[#5398 == 1] AND [#5397 == 0]]  ; user pressed OK AND render mode is off \n'
          '    ' + get_gcode_rapidmove(coordinate) + 'ENDIF\n\n')
def get_gcode_rapidmove(coordinate):
    return ('G00 X' +
            str(round(coordinate[0], 3)) + ' Y' +
            str(round(coordinate[1], 3)) + ' Z' +
            str(round(coordinate[2], 3)) + '\n')

def get_info_z_min(zmin):
    return 'MSG "Maximum Z cutting depth: ' + str(round(zmin, 3)) + '"\n\n'

if __name__ == "__main__":
    hello()
