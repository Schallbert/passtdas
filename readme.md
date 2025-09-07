# *passtdas*
![Image: A symbolic image of what *passtdas* does](/assets/*passtdas*.png)

*passtdas* is a small command-line helper application written in Python that takes a G-code file,
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
*passtdas* has no mandatory argument.

## Parameters
*passtdas*'s parameters:
1. `--file` or `-f`: The source file to be analyzed. This parameter is required.
2. `--zsafety` or `-s` The safety height you want the machine to run to the XY extreme points.
3. `--zprobe` or `-p` The probe height the machine will go to at the extreme points to simplify manual adjustments
of workpiece position.
This Z parameters are optional. 

The two optional parameters default to `zsafety=40mm` and `zprobe=15mm` if no or an erroneous value is given.

## Dialog
The Beta version 0.9.4 requires a `MSG` command to inform the user about the next 
extreme value to pinpoint. Thus, the CNC interpreter needs to understand that command.
I'm also using a pause command `M00` to have the user press the **Start** button for each pinpoint.

## How to create and run an executable
The application Python's supports **setuptools**. The following steps assume you have a virtual python environment that
can run Python's package manager **pip**.

To deploy, type the following commands in a shell within the root folder of this project:
- `python setup.py --quiet bdist_egg` This will create an eggfile that can just be installed using pip.
- `.\venv\Scripts\Activate.ps1` Activates the virtual environment in your venv folder
- `pip install --editable .` Installs the eggfile
- `*passtdas* -f "./test/arcg02ij.tap" -s 30 -p 10` runs the program with custom safety and probe height. just use your path.

## Example
You can run the script from command line like this:

![Image: running *passtdas* from command line](/assets/example_executefromconsole.jpg)

Alternatively, you can deploy an executable and enter the parameters later:
![Image: running *passtdas* directly as an Application](/assets/example_executeasapp.jpg)

This is how the output file for a circle of `r=5.66`, `Pcenter(0|0)` will look like.
The machine will start at XY0 and probe down to a given height. It will then pause using command `M00`.
As soon as the user hits 'start', the machine will probe the job's extreme points starting with Y-.
When complete, the machine will return to XY0 at safety height.
```ruby
G90

MSG "Zmin of this job: -1.0"
G00 Z40
G00 X0 Y0
G01 Z15 F1200

MSG "PathPreview: Hit START to go to Ymin: ['0.0', '-5.66']"
M00
G00 Z40
G00 X0.0 Y-5.66
G01 Z15 F1200

MSG "PathPreview: Hit START to go to Xmin: ['-5.66', '0.0']"
M00
G00 Z40
G00 X-5.66 Y0.0
G01 Z15 F1200

MSG "PathPreview: Hit START to go to Ymax: ['0.0', '5.66']"
M00
G00 Z40
G00 X0.0 Y5.66
G01 Z15 F1200

MSG "PathPreview: Hit START to go to Xmax: ['5.66', '0.0']"
M00
G00 Z40
G00 X5.66 Y0.0
G01 Z15 F1200

MSG "PathPreview: Hit START to go to X0 Y0 Z40: ['0', '0']"
M00
G00 Z40
G00 X0 Y0
G01 Z40 F1200

M30
```