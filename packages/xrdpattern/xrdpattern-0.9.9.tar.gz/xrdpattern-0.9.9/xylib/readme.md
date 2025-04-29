## About

Python library for XrdPatterns including import from data files, export as json file and postprocessing functionalities.
The data file import functionalities are built on C++ library  [xylib](https://github.com/wojdyr/xylib) so beyond a standard python install this library also requires:
- A C++ compiler and standard library
- A C++ to python bridge (Swig)

It allows for (lotsa things)


## Setup

### System level requirements
For Ubuntu 22.04:
```
sudo apt install build-essential	# GNU C++ compiler
sudo apt install libboost-all-dev       # C++ libraries provided by Boost
sudo apt install swig 			# python -> C++ bridge
```

For Windows >10 you may try the following in PowerShell (requires [Chocolatey](https://chocolatey.org/)):
```
choco install mingw  # C++ compiler and std library
choco install swig   # python -> C++ bridge
```
### Python library
Once the system level requirements are installed, the library can be installed using pip:
```
pip install xrdpattern
```
