# cncPathPreview
![Image: A symbolic image of what cncPathPreview does](/assets/cncpathpreview.png)

CNCpathpreview is a small command-line helper application written in Python that takes a G-code file,
reads its Move-commands `(G00, G01, G02, G03)` and determines maximum and
minimum values for its movements in `X` and `Y` direction.

These values are then written to an output file that can be run as a `Jobfile`
by the CNC application to check whether the CNC paths are within dimensions of the workpiece.

## Which problem does it solve?
- You are unsure where to position your workpiece
- You do not know if your milling paths fit on the workpiece

## Features
Detects "extreme values" of any given move command including arcs that have
multiple possible values. Supports `G92` coordinate shift and takes them into account.

## Arguments
CNCpathPreview has no mandatory argument.

## Parameters
CNCpathPreview's parameters:
1. `--file` or `-f`: The source file to be analyzed. This parameter is required.
2. `--zsafety` or `-z` The safety height you want the machine to run to the XY extreme points.
This parameter is optional. It defaults to `25mm` if no or an erroneous value is given.

## Dialog
The Beta version 0.93 requires a `MSG` command to inform the user about the next 
extreme value to pinpoint. Thus, the CNC interpreter needs to understand that command.
I'm also using a pause command `M00` to have the user press the **Start** button for each pinpoint.

## How to create and run an executable
The application Python's supports **setuptools**.
run `setup.py` in a shell using the following commands:
- `python setup.py --quiet bdist_egg` This will create an eggfile that can just be installed using pip.
- `.\venv\Scripts\Activate.ps1` Activates the virtual environment in your venv folder
- `pip install --editable .` Installs the eggfile
- `cncpathpreview "./test/arcg02ij.tap" -z 10` runs the program, just use your path.

## Example
You can run the script from command line like this:

![Image: running cncPathPreview from command line](/assets/example_executefromconsole.jpg)

Alternatively, you can deploy an executable and enter the parameters later:
![Image: running cncPathPreview directly as an Application](/assets/example_executeasapp.jpg)

This is how the output file for a circle of `r=5.66`, `Pcenter(0|0)` will look like:
```ruby
G90

MSG "Zmin of this job: -1.0"
G00 X0 Y0 Z10.0
MSG "PathPreview: Hit START to go to Ymin: ['0.0', '-5.66', '10.0']"
M00
G00 X0.0 Y-5.66 Z10.0

MSG "PathPreview: Hit START to go to Xmin: ['-5.66', '0.0', '10.0']"
M00
G00 X-5.66 Y0.0 Z10.0

MSG "PathPreview: Hit START to go to Ymax: ['0.0', '5.66', '10.0']"
M00
G00 X0.0 Y5.66 Z10.0

MSG "PathPreview: Hit START to go to Xmax: ['5.66', '0.0', '10.0']"
M00
G00 X5.66 Y0.0 Z10.0

M30
```