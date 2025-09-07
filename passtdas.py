import sys
from enum import Enum
import click
from os import path
from math import sqrt, acos, cos, sin, atan, pi, degrees, isclose

# Author: "Schallbert"
# Created: 2023
VERSION = '0.9.4'
# License: GPL V3

class MoveType(Enum):
    NONE = 0
    LINEAR = 1
    ARC_CLOCKWISE = 2
    ARC_ANTICLOCK = 3

def is_move(command):
    """Checks if input G-code line is a move (linear or arc) command.
    @:param command: The G-code input line
    @:return A MoveType Enum according to the move type."""
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
    coordinate = [None, None, 0, None, None, None]
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
    return min(data, key=lambda i: i[column_index])

def get_arc_degrees(coordinates):
    """Calculates an arc's span from a given point on the arc, arc's center point and a radius
    @:param coordinates: the input coordinate list
    @:return arc's length in degrees"""
    if coordinates[5] <= 0:
        return 0
    cosinus = (coordinates[0] - coordinates[3]) / coordinates[5]  # cos = deltax / radius
    if cosinus > 1:
        cosinus = 1
    elif cosinus < -1:
        cosinus = -1
    rad = acos(cosinus)
    if coordinates[1] < coordinates[4]:
        #  negative y, count from 360° backwards
        rad = 2 * pi - rad
    return round(degrees(rad), 1)

def remove_duplicate(input_list, compare):
    """Helper method that runs through a list of coordinates, only adding the compared input if it is not already
    present. Not a very pythonic implementation, I know, but it was quick to write ;)
    @:param input_list: the list to check for duplicates
    @:param compare: the list to compare the input to
    @:return the resulting list"""
    for item in input_list:
        duplicate = True
        for i in range(0, len(item)):
            duplicate &= isclose(item[i], compare[i], rel_tol=0.01)
        if duplicate:
            return input_list
    input_list.append(compare)
    return input_list

def get_extremes_from_arc(arc, coordinates):
    """Calculator function that returns minimum one but up to five possible extreme points from an arc definition.
    @:param arc: list containing angles for arc_start and arc_end
    @:param coordinates : target xyz position, arc_center xy, arc radius
    @:return a list of xyz coordinates with arc's extreme values"""
    # min/max calculations needed later on
    xyz = [coordinates[0], coordinates[1], coordinates[2]]
    radius = coordinates[5]
    center_x = round(coordinates[3], 2)
    center_y = round(coordinates[4], 2)
    x_plus_radius = [center_x + radius, center_y, xyz[2]]
    y_plus_radius = [center_x, center_y + radius, xyz[2]]
    x_minus_radius = [center_x - radius, center_y, xyz[2]]
    y_minus_radius = [center_x, center_y - radius, xyz[2]]
    extremevalue_order = [x_plus_radius, y_plus_radius, x_minus_radius, y_minus_radius]
    if (arc[1] - arc[0]) < 0:
        # crossing the 0° line (x-axis), handle overflow with nested if below
        arc[1] += 360
    result = []
    for crossing_angle in range(0, 721, 90):
        if crossing_angle in range(int(arc[0]), int(arc[1] + 1)):
            i = int(crossing_angle / 90)
            if i > 3:
                i -= 4
            result.append(extremevalue_order[i])
    return remove_duplicate(result, xyz)

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

def get_arc_angles(coordinates, previous_coordinates, move_type):
    """Simple determination of start and end angle of an arc."""
    if move_type == MoveType.ARC_CLOCKWISE:
        arc_start = get_arc_degrees(coordinates)
        arc_end = get_arc_degrees(previous_coordinates)
    else:
        arc_start = get_arc_degrees(previous_coordinates)
        arc_end = get_arc_degrees(coordinates)
    return [arc_start, arc_end]

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
    p1p2_distance_center = sqrt(coordinates[5] ** 2 - ((p1p2_distance / 2) ** 2))

    #  case handling where atan is not defined (90°, 270°)
    if p1p2_distance_y == 0:
        cosinus = 0
        sinus = 1
    else:
        p1p2_90degslope = atan(p1p2_distance_x / p1p2_distance_y)
        cosinus = abs(cos(p1p2_90degslope))
        sinus = abs(sin(p1p2_90degslope))
    #  handle quadrant changes (doesn't work with multiple quadrant moves yet :'(
    if ((p1p2_distance_x < 0 and move_type == MoveType.ARC_CLOCKWISE) or
            (p1p2_distance_x > 0 and move_type == MoveType.ARC_ANTICLOCK)):
        sinus *= -1
    if ((p1p2_distance_y > 0 and move_type == MoveType.ARC_CLOCKWISE) or
     (p1p2_distance_y < 0 and move_type == MoveType.ARC_ANTICLOCK)):
        cosinus *= -1

    coordinates[3] = p1p2_midpoint_x - cosinus * p1p2_distance_center
    coordinates[4] = p1p2_midpoint_y - sinus * p1p2_distance_center
    previous_coordinates = fill_previous_coordinates(coordinates, previous_coordinates)

    arc = get_arc_angles(coordinates, previous_coordinates, move_type)
    return get_extremes_from_arc(arc, coordinates)

def handle_arc_move_ij(coordinates, previous_coordinates, move_type):
    """handles an arc move command by finding out arc radius, span, and position.
    It then finds the arc's extreme values and returns them.
    @:param coordinates: the target move coordinates
    @:param previous_coordinates: a valid target coordinate from the past
    @:param move_type: An enum indicating arc direction
    @:return one or multiple valid coordinates depending on arc length and position or empty list in case of an error."""
    coordinates[5] = sqrt(coordinates[3] ** 2 + coordinates[4] ** 2)
    #  calculate arc_center from ij_offset and previous XY coordinates
    coordinates[3] = previous_coordinates[0] + coordinates[3]
    coordinates[4] = previous_coordinates[1] + coordinates[4]
    previous_coordinates = fill_previous_coordinates(coordinates, previous_coordinates)

    arc = get_arc_angles(coordinates, previous_coordinates, move_type)
    return get_extremes_from_arc(arc, coordinates)

def fill_previous_coordinates(coordinates, previous_coordinates):
    otherarcpoint = [0, 0, 0, 0, 0, 0]
    otherarcpoint[0] = previous_coordinates[0]
    otherarcpoint[1] = previous_coordinates[1]
    otherarcpoint[2] = previous_coordinates[2]
    otherarcpoint[3] = coordinates[3]
    otherarcpoint[4] = coordinates[4]
    otherarcpoint[5] = coordinates[5]
    return otherarcpoint

def create_dataset_from_input(file):
    """Reads a G-code input file and generates coordinate sets for every move command.
    @:param file: the file that shall be read
    @:return data: a list of coordinates"""
    data = []
    with file as f:
        lines = f.readlines()

        previous_coordinates = [None, None, None]
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
            if coordinates[0] is None or coordinates[1] is None:
                continue
            if move_type == MoveType.LINEAR:
                data.append([coordinates[0], coordinates[1], coordinates[2]])
            else:
                if coordinates[5]:
                    #  arc move with given radius
                    extreme_values = handle_arc_move_r(coordinates, previous_coordinates, move_type)
                else:
                    #  arc move with given arc center coordinates
                    extreme_values = handle_arc_move_ij(coordinates, previous_coordinates, move_type)
                data.extend(extreme_values)
            previous_coordinates = coordinates
    return data

def generate_output_file(target_filename, data, zinfo):
    """Creates a new G-code file and writes minimum and maximum coordinate values along with a dialog
    for the machine user to adjust workpiece position if necessary.
    @:param target_filename: the output filename
    @:param data: the input coordinate set
    @:param zinfo: a list containing zsafety and zprobe height on which the extreme coordinate values are approached"""
    try:
        with open(target_filename, 'w') as f:
            click.echo('Info: Writing to target file ' + click.style(target_filename, fg="green"), err=False)
            f.write(get_file_header(target_filename))
            f.write(get_extreme_value('Zmin', data))  # Print Zmin
            f.write(get_zxyzmove(['0', '0'], zinfo))  # Go to X0Y0

            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            extremes = get_extremes_text(targets, data)
            for i in range(0, len(targets)):
                f.write(get_command_strings(targets[i], extremes[i], zinfo))
            f.write(get_command_strings('X0 Y0 Z' + zinfo[0], ['0', '0'], [zinfo[0], zinfo[0]]))  # back to X0Y0
            f.write('M30')
            f.close()
    except FileExistsError:
        click.secho('Error: Could not create file.', err=True, fg="red")

def get_extremes_text(targets, data):
    """Extracts a list of extreme values from data using targets string for filtering.
    @:param targets: a list of strings with extreme value targets
    @:param data: the move dataset
    @:return list of strings containing extreme coordinates"""
    extremes = []
    for axis in targets:
        extremes.append(get_extreme_value(axis, data))
    return extremes


def get_extreme_value(axis, data):
    """Finds minimum and maximum values within a set of data for a given axis.
    @:param axis: A string defining axis and extreme value to find, e.g. `Xmin`
    @:param data: A list of lists, each entry containing XYZ coordinates
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
    stringresult = [str(round(result[0], 3)), str(round(result[1], 3))]
    click.echo(f'Found ' + axis + ' at coordinates ' + ' | '.join(stringresult), nl=True)
    return stringresult

def get_file_header(targetfilename):
    """Function that creates boilerplate comments for the output G-code file header.
    @:param targetfilename: String that defines the targeted output file
    @:return a String object"""
    return ('(PasstDas by Schallbert, 2023)\n'
            '(Version: ' + VERSION + ')\n'
            '(File output is supplied without liability.)\n'
            '(Output paths must be checked for correctness before usage.)\n'
            '(Make sure you measure Z0 of your workpiece BEFORE starting.)\n\n'
            '(Source project: ' + targetfilename + ')\n\n'
            'G90\n\n')

def echo_boilerplate():
    click.secho(message=\
"PasstDas CNC-Pfadvorschau V" + VERSION + "\n\
Autor: Schallbert\n\
Distributor: technische Dienstleistungen Preusser\n\
Copyright: 2023\n\
Veroeffentlicht unter: GNU GPL V3\n\
Blog: https://schallbert.de\n\
WARNUNG: Ausgabe des Programms ohne Gewaehr!\n", fg='blue')

def get_command_strings(axis, coordinate, zinfo):
    """Creates G-code message and pause command along with a target rapid move to head for the next extreme value
    @:param axis: The axis description
    @:param coordinage: The coordinates to be written
    @:return a String object"""
    return ('MSG "PathPreview: Hit START to go to ' + axis + ': ' + str(coordinate) + '"\n'
            + 'M00\n'
            + get_zxyzmove(coordinate, zinfo))

def get_zxyzmove(coordinate, zinfo):
    """Simple helper to build a rapid move command
    @:param coordinate: input list of coordinate strings
    @:return a String object"""
    return ('G00 Z' + zinfo[0] + '\n' +
            'G00 X' + coordinate[0] + ' Y' + coordinate[1] + '\n'
            'G01 Z' + zinfo[1] + ' F1200' +'\n\n')

def convert_int_unsigned(value):
    """Helper method that evaluates a user input and provides a default value on error
    @:param value: An integer value
    @:return the validated number as positive integer"""
    if value <= 0:
        click.secho('Warning: ' + str(value) + ' might lead to machine crash. Defaulting to Z=40.', err=True, fg="yellow")
        value = 40
    return str(value)

@click.command()
@click.option("-f", "--file", prompt="Enter source file path like so: <path/to/my/gcodefile.cnc>",
              help="The file to analyze for CNC job area edge detection",
              default=None, show_default=True, type=click.File(mode="r"), required=True )
@click.option("-s", "--zsafety", prompt="Enter positive Z-safety height",
              help="Safety Z-height on which the CNC will move to targeted coordinates",
              default=40, show_default=True, type=int, required=False)
@click.option("-p", "--zprobe", prompt="Enter positive Z-probe height",
              help="Probing Z-height to which the CNC will move when target XY coordinates are reached\
               to simplify optical dimensions check",
              default=15, show_default=True, type=int, required=False)
def path_preview(file, zsafety, zprobe):
    """A small command-line application that takes a G-code file and traces dimensions of the cutting paths.
    Its output is another G-code file to check if the workpiece fits the planned paths."""
    target_path = path.dirname(file.name)
    target_filename = 'passtdas_' + path.basename(file.name)

    data = create_dataset_from_input(file)
    if not data:
        click.secho('Error: Could not find G-code move commands in source file.', err=True, fg="red")
    else:
        click.secho('Info: Successfully read G-code move commands in source file: ' + file.name, fg="green")
        generate_output_file(path.join(target_path, target_filename), data,
                             [convert_int_unsigned(zsafety), convert_int_unsigned(zprobe)])

    click.confirm("Press <Return> to quit", default=True)

# add pyinstaller hook for deployment
if getattr(sys, 'frozen', False):
    echo_boilerplate()
    path_preview()

# add run hook for IDE
if __name__ == "__main__":
    echo_boilerplate()
    path_preview()
