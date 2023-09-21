import click
from math import sqrt

def has_move_command(line):
    if line:
        return line.find('G00') > -1 or line.find('G01') > -1


def has_arc_command(line):
    if line:
        return line.find('G02') > -1 or line.find('G03') > -1


def parse_coordinates(line):
    values = line.split(' ')
    coordinate = [0, 0, 25, 0, 0]
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

def handle_start_state_overflow(state):
    if state > 3:
        state -= 4
    return state

def get_arc_case(coordinates):
    xy = 0
    xy += 2*((coordinates[0]-coordinates[3]) >= 0)  # x positive? +2
    xy += (coordinates[1]-coordinates[4]) >= 0  # y positive? +1
    return xy

def handle_arc_commands(previous_coordinates, line):
    coordinates = parse_coordinates(line)
    if line.find('G02') > -1:
        previous_coordinates[3] = coordinates[3]
        previous_coordinates[4] = coordinates[4]
        end_state = get_arc_case(previous_coordinates)
        start_state = get_arc_case(coordinates)

    elif line.find('G03') > -1:
        previous_coordinates[3] = coordinates[3]
        previous_coordinates[4] = coordinates[4]
        end_state = get_arc_case(coordinates)
        start_state = get_arc_case(previous_coordinates)
    else:
        return [] #  command does not fit move pattern and will not count.

    # min/max calculations needed later on
    xyz = [coordinates[0], coordinates[1], coordinates[2]]
    radius = sqrt(coordinates[3] ** 2 + coordinates[4] ** 2)
    x_plus_radius = [coordinates[3] + radius, coordinates[1], coordinates[2]]
    y_plus_radius = [coordinates[0], coordinates[4] + radius, coordinates[2]]
    x_minus_radius = [coordinates[3] - radius, coordinates[1], coordinates[2]]
    y_minus_radius = [coordinates[0], coordinates[4] - radius, coordinates[2]]
    extremevalue_order = [y_minus_radius, x_minus_radius, x_plus_radius, y_plus_radius]

    statediff = end_state - start_state
    print(radius)
    print(line)
    print(start_state)
    print(end_state)
    # same quadrant?
    if statediff == 0:
        if previous_coordinates[start_state] >= coordinates[start_state]:
            # near full circle, return all four possible max/min points
            statediff = 4

    result = []
    print(statediff)
    # crossing one, two or three quadrants
    for i in range(statediff):
        print(i)
        result.append(extremevalue_order[start_state + i])

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

        previous_xy_command = []
        for line in lines:
            line = line.strip()
            if has_move_command(line):
                data.append(parse_coordinates(line))
            if has_arc_command(line):
                lines = handle_arc_commands(previous_xy_command, line)
                if lines:
                    data.extend(lines)
            if data:
                if data[-1][0] != 0 and data[-1][1] != 0:
                    previous_xy_command = data[-1]

    # data = list(enumerate(data))  # create enumerated list out of data
    #print(get_max_by_column(data, 1))
    #print(get_min_by_column(data, 1))


if __name__ == "__main__":
    hello()
