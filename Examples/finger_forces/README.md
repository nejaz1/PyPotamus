# Installation instructions for finger forces task

### Install Python using Anaconda

You first need a distribution of python, we highly recommend using the Anaconda 3.6 distribution which you can get from [here](https://www.anaconda.com/downloads).

### Get the PyPotamus repository from Github

Clone the [PyPotamus](https://github.com/nejaz1/PyPotamus) repository onto your system using the following commands. For example, in  MacOSX open up a terminal window and go to the directory you want to install PyPotamus in and type the following commands:

```
mkdir PyPotamus
git clone git@github.com:nejaz1/PyPotamus.git PyPotamus
```

### [IMPORTANT] SDL Libraries

On some systems, building PyPotamus might give an error that `SDL.h` was not found. On such systems, it is important to install the SDL development tools/libraries provided [here](https://www.libsdl.org/download-2.0.php).

### Install package dependencies for PyPotamus

Use the condo package manager to setup a new environment and install the package dependencies specified in the `environment.yml` file using the following commands in terminal:

```
cd PyPotamus
conda env create -f environment.yml
```

### Run the finger task

Switch to the newly created environment and run the task using terminal:

```
source environment PyPotamus
cd PyPotamus/Examples/finger_forces
python main.py
```


This will open up the experiment display windows, which you can manipulate using commands in the python window. Use the following command to setup a subject with id `s01` and run the sequence of finger tests specified in the file `demo_r3.tgt`

```
subj s01
run 1 demo_r3.tgt
```

### 



