# Mosaicode

A Visual Programming Environment and source code generator for specific domains, focusing on Digital Art.

## Getting Started

Getting a copy of the project up and running on your local machine. Supported Platform: GNU/Linux.


### Prerequisites

Open the terminal (Ctrl+Alt+T) and run the following command to install the software dependencies:

```
sudo apt install python3 python3-gi python3-cairo python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev python3-dev build-essential pkg-config python3-pip python3-venv
```

**Alternative**: Use the Makefile for automatic installation:

```
make install_full
```

### Installation

Steps to install the Mosaicode in a virtual environment or in the operational system directory.


#### Virtual Environment / Isolated from system directories

Installing python virtual environment via terminal:

```
sudo apt install python3.8-venv
```

Setting the virtual environment:

1. Create the environment: `python3 -m venv <virtual environment name>`
1. Active the environment: `source <virtual environment path>/<virtual environment name>/bin/activate`
1. Install prerequisites: `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev`
1. Install PyGObject: `python -m pip install PyGObject`
1. Install Mosaicode: `python setup.py install`

**Alternative**: Use the Makefile for automatic virtual environment setup:

```
make install_venv
```

More details in the Python 3 *Virtual Environments and Packages* documentation: https://docs.python.org/3/tutorial/venv.html

#### Operational System Directories

Run via terminal:

```
sudo python setup.py install
```

**Alternative**: Use the Makefile for system installation:

```
make install_full
```

### Useful Makefile Commands

- `make help` - Show all available commands
- `make check_deps` - Check if dependencies are properly installed
- `make run` - Run Mosaicode in development mode
- `make run_installed` - Run installed Mosaicode
- `make test_normal` - Run tests
- `make clean` - Clean build files

## Mosaicode Extensions

Some extensions that you can install to add visual programming languages with resources from areas of computing which allow the development of tools to support Digital Art in a simple and practical way: dragging and connecting blocks:


| Technology  	                | Domain  	         | Extension repository  	                                          | Operating |
| ---	                          | ---	               | ---	                                                            | ---       |
|  Javascript / Web Audio API   | Computer Music  	 | https://github.com/Alice-ArtsLab/mosaicode-javascript-webaudio  	| Yes        |
|  C / OpenCV  	              	| Computer vision  	 | https://github.com/Alice-ArtsLab/mosaicode-c-opencv              | No        |
|  C / Opengl 	    	          | Computer graphics  | https://github.com/Alice-ArtsLab/mosaicode-c-opengl              | No        |
|  Javascript / Canvas 	        | Graphics on a web  | https://github.com/Alice-ArtsLab/mosaicode-javascript-canvas     | No        |
|  C / Linux-Joystick	          | USB Controller  	 | https://github.com/Alice-ArtsLab/mosaicode-c-joystick            | No        |
|  C / Gtk 	                    | GUI                | https://github.com/Alice-ArtsLab/mosaicode-c-gtk                 | No        |
|  C / Portaudio 	              | Computer Music  	 | https://github.com/Alice-ArtsLab/mosaicode-c-sound               | No        |



## Related pages

ALICE. Lab:  [https://alice.dcomp.ufsj.edu.br/](https://alice.dcomp.ufsj.edu.br/)

## Contact

Asking to:

* mosaicode-dev@googlegroups.com
