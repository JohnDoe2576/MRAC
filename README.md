# Neural Network based Model Reference Adaptive Controller (Python)
This is part of a code that generates a **M**odel **R**eference **A**daptive **C**ontroller. The plant can be modelled either with a 
a. Neural Network architecture or
b. SINDy (**S**parse **I**dentification of **N**onlinear **Dy**namics) architecture.

The controller has a Neural Network architecture.

The code can be used for MRAC development for the following nonlinear systems.
1. Magnetic Levitation System
2. Robotic Arm System
3. Van Der Pol oscillator

The procedure for controller development is as follows, wherein a tick shows the project completion.
- [x] Excite the plant using **A**mplitude Modulated **P**seudo **R**andom **B**inary **S**equence and obtain Input-Output data 
- [ ] Train a Neural Network/SINDy model for the plant using Pytorch/Numpy respectively
- [ ] Excite the tracking system with APRBS and obtain the Input-Output data
- [ ] Connect the trained plant model to a Neural Network model for the controller and train the controller network
- [ ] Couple this controller to the actual plant and show control

Please note that the [Matlab implementation](https://github.com/JohnDoe2576/VanDerPol) for this is complete (- the SINDy model), and the Python implementation is ongoing.

## Code structuring
The code is Object-Oriented, and three-layered as detailed below.
- **Layer 1**: `Main.py` is the upper-most layer, a class wherein the `user enters the required parameters`
- **Layer 2**: `MRAC_Sim.py` is the second layer, the _core of code_, a class wherein the `controller development procedure is detailed`
- **Layer 3**: `Generate_Data.py`, `Dynamic_Systems.py`, `Data_Handler.py`, `Parameters.py` and `Plot_Data.py` are classes which are `dependencies for the upper layers`; naming justifies their working

The standard Python modules required are `Numpy`, `Scipy`, `Pandas`, `Pickle`, `bz2file`, `Matplotlib`
