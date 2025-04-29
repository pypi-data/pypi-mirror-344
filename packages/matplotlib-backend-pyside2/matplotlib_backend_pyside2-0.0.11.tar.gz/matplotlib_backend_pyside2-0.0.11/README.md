# Acknowledgement

This is a fork from [Jovan Mitrevski](https://github.com/jmitrevs/matplotlib_backend_qtquick).
All credit for this project goes to him. 

This fork removes the dependency on PyQt.

## Installation

Since we include a fixed version of PySide2 on our measurement devices, the `PySide2` package is handled as an optional dependency. Do not install or update `PySide2` on an Optimizer4D device since it will most likely break the Analyzer4D software!

Installation on a device without the Analyzer4D software:
```sh
pip install matplotlib_backend_pyside2[pyside2]
```
