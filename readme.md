# cncPathPreview
is a small command-line helper application written in Python that takes a G-code file,
reads its Move-commands `(G00, G01, G02, G03)` and determines maximum and
minimum values for its movements in `X` and `Y` direction.

These values are then written to an output file that can be run as a `Jobfile`
by the CNC application to check whether the CNC paths are within dimensions of the workpiece.

## Which problem does it solve?
- You are unsure how to position your workpiece
- You do not know if your milling paths fit on the workpiece

## Features
Detects "extreme values" of any given move command including arcs that have
multiple possible values. Supports `G92` coordinate shift and takes them into account.

## Arguments
CNCpathPreview only has one mandatory argument: The path of its input file.

Example call: `cncPathPreview.py "path/to/my/jobfile.tap"`

## Parameters
CNCpathPreview's parameter:

`--zsafety`: The safety height you want the machine to run to the XY extreme points.
It defaults to `25mm` if no or an erroneous value is given.

## Dialog
Current Alpha version only supports *EdingCNC* syntax and thus uses a command called
`DLGMSG` to ask the user whether the next extreme point shall be moved to.

## Limitations
Features to be added (soon):
- Add `G02/G03 X Y R` syntax handling
- Add installer
- Add scratch parameter