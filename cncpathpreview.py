from enum import Enum
import click
from math import sqrt, acos, cos, atan, pi, degrees

class MoveType(Enum):
    NONE = 0
    LINEAR = 1
    ARC_CLOCKWISE = 2
    ARC_ANTICLOCK = 3


def is_move(command):
    """Checks if input G-code line is a move (linear or arc) command.
    @:param command: The G-code input line
    @:return A MoveType Enum according to the move type.."""
    if command:
        if (command.find('G00') > -1 or (command.find('G0 ') > -1) or
            command.find('G01') > -1) or (command.find('G1 ') > -1):
                return MoveType.LINEAR
        if (command.find('G02') > -1) or (command.find('G2 ') > -1):
            return MoveType.ARC_CLOCKWISE
        if (command.find('G03') > -1) or (command.find('G3 ') > -1):
            return MoveType.ARC_ANTICLOCK
    return MoveType.NONE

def is_coordinate_shift(command):
    """Checks if input G-code line is a coordinate shift command.
        @:param command: The G-code input line
        @:return True if the line is a shift command, False if not."""
    if command:
        return command.find('G92') > -1
    return False

def parse_coordinates(line):
    """Reads a move command and converts it into a float value set
    @:param line: a move command
    @:return a float value set."""
    values = line.split(' ')
    coordinate = [None, None, None, None, None, None]
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
        if value.find('R') > -1:
            coordinate[5] = float(value.strip('R '))
    return coordinate


def get_max_by_column(data, column_index):
    """Returns a subset of entries that reflect a maximum value based on input column
    @:param data: the input list
    @:param column_index: the column to find the max for
    @:return the line that contains the maximum value of a given column"""
    return max(data, key=lambda x: x[column_index])

def get_min_by_column(data, column_index):
    """Returns a subset of entries that reflect a minimum value based on input column
    @:param data: the input list
    @:param column_index: the column to find the max for
    @:return the line that contains the maximum value of a given column"""
    return min(data, key=lambda x: x[column_index])

def get_arc_degrees(coordinates, arc_center, radius):
    """Calculates an arc's span from a given point on the arc, arc's center point and a radius
    @:param coordinates: the input vector
    @:param arc_center: coordinates of the arc's center
    @:param: arc radius: scalar indicating the arc's radius
    @:return arc's length in degrees"""
    if radius <= 0:
        return 0
    cosinus = round((coordinates[0] - arc_center[0]) / radius, 3)  # cos = deltax / radius
    rad = acos(cosinus)
    if (coordinates[1] - arc_center[1]) < 0:
        #  negative y, count from 360° backwards
        rad = 2*pi - rad
    return round(degrees(rad), 0)

def fill_coordinates(coordinates, previous_coordinates, shift):
    """helper that removes 'None' values from a line by filling with last known coordinate values and applies
    coordinate shifts
    @:param coordinates: the current target vector
    @:param previous_coordinates: valid target vector from the past
    @:param shift: the shifted coordinate system
    @:return the filled coordinate vector"""
    for i in range(0, 3):
        #  Only fill XYZ (0-2)
        if coordinates[i] is None:
            coordinates[i] = previous_coordinates[i]
        else:
            coordinates[i] += shift[i]
    return coordinates

def handle_coordinate_shift(line, shift):
    """Checks how the coordinate system has been shifted. Returns the shift to be superpositioned onto move commands.
    @:param line: The input command line
    @:param shift: The current shift coordinates XYZ
    @:return shift: the updated coordinate shift XYZ"""
    coordinate_system_shift = parse_coordinates(line)
    for i in range(0, 3):
        if coordinate_system_shift[i]:
            # coordinate shifted.
            shift[i] -= coordinate_system_shift[i]
    return shift

def handle_linear_move(coordinates):
    """handles a linear move command by parsing into floats, filling in 'None values'.
    @:param line: an input command, previous_coordinates: a valid target coordinate from the past
    @:return a valid coordinate"""
    return [coordinates[0], coordinates[1], coordinates[2]]

def handle_arc_move_r(coordinates, previous_coordinates, move_type):
    """handles an arc move command by finding out arc span and position.
        It then finds the arc's extreme values and returns them.
        @:param coordinates: the target move coordinates
        @:param previous_coordinates: a valid target coordinate from the past
        @:param move_type: An enum indicating arc direction
        @:return one or multiple valid coordinates depending on arc length and position or empty list in case of an error."""
    p1p2_midpoint_x = (coordinates[0] + previous_coordinates[0]) / 2
    p1p2_midpoint_y = (coordinates[1] + previous_coordinates[1]) / 2
    p1p2_distance_x = coordinates[0] - previous_coordinates[0]
    p1p2_distance_y = coordinates[1] - previous_coordinates[1]
    p1p2_distance = sqrt(p1p2_distance_x ** 2 + p1p2_distance_y ** 2)

    if p1p2_distance == 0:
        return [None, None, None]
    p1p2_90degslope = -(p1p2_distance_x / p1p2_distance_y)
    angle = atan(p1p2_90degslope)
    arc_height = coordinates[5] - sqrt(coordinates[5] ** 2 - ((p1p2_distance / 2) ** 2))

    center_x = p1p2_midpoint_x + cos(angle) * (coordinates[5] - arc_height)
    if move_type == MoveType.ARC_ANTICLOCK:
        center_y = p1p2_midpoint_y - p1p2_90degslope * (center_x - p1p2_midpoint_x)
        arc_start = get_arc_degrees(coordinates, [center_x, center_y], coordinates[5])
        arc_end = get_arc_degrees(previous_coordinates, [center_x, center_y], coordinates[5])
    else:
        center_y = p1p2_midpoint_y + p1p2_90degslope * (center_x - p1p2_midpoint_x)
        arc_start = get_arc_degrees(previous_coordinates, [center_x, center_y], coordinates[5])
        arc_end = get_arc_degrees(coordinates, [center_x, center_y], coordinates[5])

    return get_extremes_from_arc(arc_end, arc_start, coordinates, [center_x, center_y])


def handle_arc_move_ij(coordinates, previous_coordinates, move_type):
    """handles an arc move command by finding out arc radius, span, and position.
    It then finds the arc's extreme values and returns them.
    @:param coordinates: the target move coordinates
    @:param previous_coordinates: a valid target coordinate from the past
    @:param move_type: An enum indicating arc direction
    @:return one or multiple valid coordinates depending on arc length and position or empty list in case of an error."""
    radius = sqrt(coordinates[3] ** 2 + coordinates[4] ** 2)
    arc_center = (previous_coordinates[0] + coordinates[3], previous_coordinates[1] + coordinates[4])

    if move_type == MoveType.ARC_CLOCKWISE:
        arc_start = get_arc_degrees(coordinates, arc_center, radius)
        arc_end = get_arc_degrees(previous_coordinates, arc_center, radius)
    else:
        arc_start = get_arc_degrees(previous_coordinates, arc_center, radius)
        arc_end = get_arc_degrees(coordinates, arc_center, radius)

    coordinates[5] = radius
    return get_extremes_from_arc(arc_end, arc_start, coordinates, arc_center)


def get_extremes_from_arc(arc_end, arc_start, coordinates, arc_center):
    # min/max calculations needed later on
    xyz = [coordinates[0], coordinates[1], coordinates[2]]
    radius = coordinates[5]
    x_plus_radius = [arc_center[0] + radius, arc_center[1], xyz[2]]
    y_plus_radius = [arc_center[0], arc_center[1] + radius, xyz[2]]
    x_minus_radius = [arc_center[0] - radius, arc_center[1], xyz[2]]
    y_minus_radius = [arc_center[0], arc_center[1] - radius, xyz[2]]
    extremevalue_order = [0, y_plus_radius, x_minus_radius, y_minus_radius, x_plus_radius]
    if (arc_end - arc_start) < 0:
        # crossing the 0° line (x-axis)
        arc_end += 360
    result = []
    for crossing_angle in range(90, 361, 90):
        if crossing_angle in range(int(arc_start), int(arc_end)):
            result.append(extremevalue_order[int(crossing_angle / 90)])
    result.append(xyz)
    return result


def create_dataset_from_input(file):
    """Reads a G-code input file and generates coordinate sets for every move command.
    @:param file: the file that shall be read
    @:return data: a list of coordinates"""
    data = []
    with file as f:
        lines = f.readlines()

        previous_coordinates = [0, 0, 0]
        shift = [0, 0, 0]
        for line in lines:
            line = line.strip()
            move_type = is_move(line)
            if move_type == move_type.NONE:
                if is_coordinate_shift(line):
                    shift = handle_coordinate_shift(line, shift)
                    click.echo(f'Found coordinate shift: X' + str(shift[0]) + ', Y' + str(shift[1]) + ' Z' + str(shift[2]))
                continue
            coordinates = fill_coordinates(parse_coordinates(line), previous_coordinates, shift)
            if move_type == MoveType.LINEAR:
                data.append(handle_linear_move(coordinates))
            else:
                if coordinates[5]:
                    #  arc move with given radius
                    extreme_values = handle_arc_move_r(coordinates, previous_coordinates, move_type)
                else:
                    #  arc move with given arc center coordinates
                    extreme_values = handle_arc_move_ij(coordinates, previous_coordinates, move_type)
                if lines:
                    data.extend(extreme_values)
            if data:
                previous_coordinates = data[-1]
    return data

def generate_output_file(target_filename, data, zsafety):
    """Creates a new G-code file and writes minimum and maximum coordinate values along with a dialog
    for the machine user to adjust workpiece position if necessary.
    @:param target_filename: the output filename
    @:param data: the input coordinate set
    @:param zsafety: the height on which the extreme coordinate values should be approached"""
    try:
        with open(target_filename, 'w') as f:
            f.write(get_file_header(target_filename))
            f.write(get_extreme_value('Zmin', data, zsafety))  # Print Zmin
            f.write(get_rapidmove(['0', '0', str(zsafety)]))  # Go to X0Y0

            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            for text in targets:
                value = get_extreme_value(text, data, zsafety)
                f.write(get_coordinate_strings(text, value))

            f.write('M30')
            f.close()
    except FileExistsError:
        click.echo('Error: Could not create file.', err=True)


def get_extreme_value(axis, data, zsafety):
    """Finds minimum and maximum values within a set of data for a given axis.
    @:param axis: A string defining axis and extreme value to find, e.g. `Xmin`
    @:param data: A list of lists, each entry containing XYZ coordinates
    @:param zsafety: The target Z height with which the preview shall run
    @:return a string representing the coordinates of the requested extreme value"""
    if axis == "Zmin":
        zmin = str(round(get_min_by_column(data, 2)[2], 3))
        click.echo(f'Found Zmin: ' + zmin)
        return 'MSG "Zmin of this job: ' + zmin + '"\n'

    result = [0, 0, 0]
    if axis == "Ymin":
        result = get_min_by_column(data, 1)
    elif axis == "Xmin":
        result = get_min_by_column(data, 0)
    elif axis == "Ymax":
        result = get_max_by_column(data, 1)
    elif axis == "Xmax":
        result = get_max_by_column(data, 0)
    result[2] = zsafety
    stringresult = [str(round(result[0], 3)), str(round(result[1], 3)), str(round(result[2], 3))]

    click.echo(f'Found ' + axis + ' at coordinates ' + ' | '.join(stringresult), nl=True)
    return stringresult

def get_file_header(targetfilename):
    """Function that creates boilerplate comments for the output G-code file header.
    @:param targetfilename: String that defines the targeted output file
    @:return a String object"""
    return ('(CNCPathPreview by Schallbert, 2023)\n'
            '(Release: 0.8)\n'
            '(File output is supplied without liability.)\n'
            '(Output paths must be checked for correctness before usage.)\n\n'
            '(Project: ' + targetfilename + ')\n\n'
            'G90\n\n')

def get_coordinate_strings(axis, coordinate):
    """Creates G-code message and pause command along with a target rapid move to head for the next extreme value
    @:param axis: The axis description
    @:param coordinage: The coordinates to be written
    @:return a String object"""
    return ('MSG "PathPreview: Hit START to go to ' + axis + ': ' + str(coordinate) + '"\n'
            + 'M00\n'
            + get_rapidmove(coordinate) + '\n')

def get_rapidmove(coordinate):
    """Simple helper to build a rapid move command
    @:param coordinate: input list of coordinate strings
    @:return a String object"""
    return ('G00 X' + coordinate[0] +
            ' Y' + coordinate[1] +
            ' Z' + coordinate[2] +'\n')

def convert_input_zsafety(zsafety):
    """Helper method that evaluates a user input and provides a default value on error
    @:param zsafety: A positive numeric value
    @:return the validated number as integer"""
    zsafety = round(zsafety, 0)
    if zsafety <= 0:
        click.echo('Error: Number invalid for safety height. Defaulting to Z=25.', err=True)
        zsafety = 25
    return zsafety

@click.command()
@click.argument("file", type=click.File(mode="r"))
@click.option("-z", "--zsafety", prompt="Enter positive Z-safety height",
              help="Safety Z-height on which the CNC will move to targeted coordinates",
              default=25, show_default=True, type=float, required=False)
def path_preview(file, zsafety):
    """A small command-line application that takes a G-code file and traces dimensions of the cutting paths.
    Its output is another G-code file to check if the workpiece fits the planned paths."""
    target_filename = 'PathPreview_' + file.name

    data = create_dataset_from_input(file)
    generate_output_file(target_filename, data, convert_input_zsafety(zsafety))

if __name__ == "__main__":
    path_preview()
