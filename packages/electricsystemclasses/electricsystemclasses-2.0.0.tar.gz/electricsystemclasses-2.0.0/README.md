# ElectricSystemClasses

A Python package providing a collection of classes for simulating electric systems. The library includes components like electric vehicles (EVs), generators, grids, storage systems, and loads. 
It is designed for use in simulations and modeling of power systems, focusing on flexible, easy-to-use components for energy management scenarios.

## Features

- **Electric Vehicles (EVs)**: Model and manage electric vehicle characteristics such as power, state-of-charge, and classification.
- **Generators**: Simulate electricity generation profiles, including scaling and adjusting the length of the profiles.
- **Grid**: Model the power exchange between the system and the grid, tracking the energy flow.
- **Storage Systems**: Simulate energy storage components, including charging and discharging behaviors.
- **Constant Load**: A basic class for representing time-invariant loads.
- **Variable Load**: A class representing time-variant loads.
- **Programmable Load With Activation**: A class for representing time-programmed loads with reactivation availability.

## Full DOC
At the bottom.

## Installation

You can install the `electricsystemclasses` package via pip.

`pip install electricsystemclasses`

## License

This project is licensed under the Server Side Public License (SSPL), Version 1.0. You may not use this file except in compliance with the License.

## Contributing

I welcome contributions to this project! If you'd like to contribute contact me. Ensure that your code adheres to the coding style of the project, and that you have tested your changes.

## Contact

email: rmmenichelli@gmail.com
Feel free to ask for clarification.

## Full DOC

The package provides a full simulation engine to study the behaviour of multiple electric components. Each component is represented by instances of different classes, each requiring different attributes.

The simulation is iterative-based and works around two main components, the `simulate` function and a user defined function representing a single time frame of simulation. The `simulate` function takes as arguments:
 
 `step_size`: the step size of the simulation in seconds `s`. Type `int` or `float`.

 `period`: the amount of hours to be simulated. The simulation works starting from zero and finishing at the value of `period`. The total simulated steps will be `period * 3600 / step_size`.

 `user_timeframe`: a function that needs to be defined by the user representing the logics within each timeframe. The name could be any, usually `timeframe` is chosen. This function need to be defined as:

    def timeframe(i, h, t):

        #user code

The function needs to be defined with three arguments representing in order:

- the iteration `i` of the simulation. To be used for any purposes and as argument of some classes methods.

- the current simulated step in hours, usually `h`. To be used for any purposes and as argument of some classes methods.

- the step size in hours, usually `t`. To be used for any purposes and as argument of some classes methods.

In each simulated step, the logics defined inside the `timeframe` function are applied. All attributes containing the power history and state of charge of instances are updated each step.

### **Classes**
 
#### **Constant Load**

The `ConstantLoad` class represents simple loads having constant power consumption. 

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"hvac"`.

 `required_power`: the power consumption of the load in `kW`. Type `float` or `int`.

##### **Attributes**

All the arguments of the `__init__`.

- `power_history`: a list containing all the simulated power values of the instance, in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_loads`: a list containing all instances of the class.

##### **Class Methods**
- `get_allLoads(cls)`: returns a list containing all instances of the class.

- `update(cls, i)`: takes as arument the iteration `i` provided by the simulation engine. It updates the attribute `power_history` if not supplied during the user defined timeframe.

##### **Instance Methods**
- `supply(self, input_power)`: if the `input_power` is less than the `required_power` the function raises an error. The load can't be supplied. In any other cases it returns the excess power, difference of `input_power` and `required_power`.

#### **Electric Vehicle (EV)**

The `EV` class represents electric vehicles.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"EV1"`.

 `max_discharge_power`: the maximum power dischargeable by the vehicle in `kW`. Type `float` or `int`.

 `max_charge_power`: the maximum power the vehicle can charge at, in `kW`. Type `float` or `int`.

 `opt_power`: the optimal charge and discharge power of the vehicle in `kW`. Type `float` or `int`.

 `capacity`: the capacity of the vehicle in `kWh`. Type `float` or `int`.

 `t_depart`: the departure time of the vehicle in `h`. Type `float` or `int`.

 `t_arrival`: the arriving time of the vehicle in `h`. Type `float` or `int`.
 
 `soc_lim_kwh`: the minimum target state of charge to be reached during the time between `t_arrival` and `t_depart`, in `kwh`. It is not guaranteed due to the `max_charge_power` limitation.

 `soc_min_kwh`: the state of charge below which the vehicle is classified as critical, meaning having really low state of charge.

##### **Attributes**

All the arguments of the `__init__`.

`soc_history_kwh`: a list containing all values of the state of charge in `kWh`. It gets filled during the simulation.

`power_history`: a list containing all the simulated power values of the instance, in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_EV`: a list containing all instances of the class.

- `crit_EV`: a list containing all vehicles having state of charge below `soc_min_kwh`.

- `norm_EV`: a list containing all vehicles having state of charge above `soc_min_kwh` and below `soc_lim_kwh`.

- `major_EV`: a list containing all vehicles having state of charge above `soc_lim_kwh`.

- `prior_EV`: a list containing all vehicles having state of charge such that if recharged at `opt_power` they will not reach the target `soc_lim_kwh`, therefore having a priority state over `norm_EV`.

##### **Class Methods**

- `classify_EV(cls, h)`: a method that classifies the instances of the class based on the logics of `crit_EV`, `norm_EV`, `prior_EV`, `major_EV`, at instance `h`. `h` is the current simulated time in hours given as attribute of the function `timeframe`.

- `charge_group(cls, group, power, t)`: a method that charges a group of vehicles equally dividing the input power. It returns the power that could had not be handled by the vehicles in the group due to power or capacity limitations.
Arguments:

    `group`: a list containing instances of the class. Could also be one of the classifying groups such as `norm_EV`. Type `list`.
 
    `power`: the input power in `kW`. Type `int` or `float`.

    `t`: the step size in hours. Given as argument of the function `timeframe`.

- `discharge_group(cls, group, power, t)`: a method that discharges a group of vehicles equally dividing the requested power. It returns the requested power that could had not be handled by the vehicles in the group due to power or capacity limitations.
Arguments:

    `group`: a list containing instances of the class. Could also be one of the classifying groups such as `norm_EV`. Type `list`.

    `power`: the requested power in `kW`. Type `int` or `float`.

    `t`: the step size in hours. Given as argument of the function `timeframe`.

- `discharge_group_prop(cls, group, power, t)`: a method that discharges a group of vehicles proportionally, dividing the requested power based on the `max_discharge_power` of the instances. It returns the requested power that could had not be handled by the vehicles in the group due to power or capacity limitations.
Arguments:

    `group`: a list containing instances of the class. Could also be one of the classifying groups such as `norm_EV`. Type `list`.

    `power`: the requested power in `kW`. Type `int` or `float`.

    `t`: the step size in hours. Given as argument of the function `timeframe`.

- `get_allEV(cls)`: returns a list containing all instances of the class.

- `getCritEV(cls)`: returns the list `crit_EV`.

- `getNormEV(cls)`: returns the list `norm_EV`.

- `getPriorEV(cls)`: returns the list `prior_EV`.

- `getMajorEV(cls)`: returns the list `major_EV`.

- `updateAllEV(cls, i)`: takes as arument the iteration `i` provided by the simulation engine. It updates the attributes `power_history` and `soc_history_kwh` if untouched during the user defined timeframe.

##### **Instance Methods**
- `charge(self, power, t)`: a method that charges an instance of the class. Takes as arguments an input power `power`, and the step size in hours `t` given in the function `timeframe`. It return the excess power that could had not be handled by the vehicle due to power or capacity limitations.

- `discharge(self, power, t)`: a method that discharges an instance of the class. Takes as arguments a discharge power `power`, and the step size in hours `t` given in the function `timeframe`. It return the excess discharge power that could had not be handled by the vehicle due to power or capacity limitations.

#### **Generator**

A class representing generators.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"pv1"`.
 
 `profile`: a list containing the values of the generated power in `kW`. Type `list` containing `int` or `float`. The length must be equal or greater than the number of simulated steps. Can be scaled and resized using instance methods `scale_profile`, `resize_profile`, and `resize_profile_to_simulation`.

##### **Attributes**

All the arguments of the `__init__`.

##### **Class Attributes**

- `all_gen`: list containing all instances of the class.

##### **Class Methods**

- `getAllGen(cls)`: returns a list of all instances of the class.

- `from_csv_column(cls, gen_id, filepath, col_index, delimiter=",", has_header=False)`: a method that creates an instance of the class based on values contained in a csv column. Takes as arguments an `id` of any type, the `filepath` of the csv file, `col_index` the column index starting from 0, the delimiter of the csv file (`default=","`),and a boolean representing if an header is present and needs to be skipped (`default=False`).


- `from_csv_row(cls, gen_id, filepath, row_index, delimiter=",", has_header=False)`: a method that creates an instance of the class based on values contained in a csv row. Takes as arguments an `id` of any type, the `filepath` of the csv file, `row_index` the row index starting from 0, the delimiter of the csv file (`default=","`),and a boolean representing if an header is present and needs to be skipped (`default=False`).

##### **Instance Methods**

- `scale_profile(self, factor)`: a method that scales the profile. Takes as input the scale factor `factor`, type `int` or `float`.

- `resize_profile(self, new_len)`: adapts the dimensions of the profile to a new length. If the new length is smaller than the current one, it randomly deletes elements, otherwise it randomly adds elements by taking the average of the two neighbours.

- `resize_profile_to_simulation(self, new_len)`: adapts the dimensions of the profile to the one needed in the simulation, defined by `step` and `period`. If the required length is smaller than the current one, it randomly deletes elements, otherwise it randomly adds elements by taking the average of the two neighbours.

- `derivative(self, i)`: returns the derivative of the instance `profile` at iteration `i`, takes `i` the iteration given in the `timeframe` as argument.

#### **Grid**

A class representing an infinite power grid.

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"poc1"`.

##### **Attributes**

All the arguments of the `__init__`.

`power_history`: a list containing all values of the grid power in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_grids`: list containing all instances of the class.

##### **Class Methods**

- `getAllGrids(cls)`: returns a list of all instances of the class.

##### **Instance Methods**

- `withdraw(self, power_value)`: a method that represents withdrawing power from a grid instance.
 

- `inject(self, power_value)`: a method that represents injecting power from a grid instance.
 
- `update(cls)`: a method that updates the instance `power_history` attribute if unchanged by the user defined logic.

#### **Programmable Load With Reactivation**

A class representing a programmable load defined:

 - a period of activation in hours, defined by a start time and an end time. This is the period in which the load can be activated, the period is defined representing as 0 hours the start of the simulation. Therefore in a simulation of a single day starting from midnight, a load that wants to be activated only between 10am and 3 pm will have start time 10 and end time 15. Only between this period the `activate(h)` function will execute.

- a minimum of active time in hours, if greater than zero the load will not be disactivated before this time has passed.

 - a reactivation boolean, representing if the load needs to be reactivated when a repeated call of the activate method happens. 

 - a deactivation delay active only for reactivable loads in seconds. 

The `__init__` takes as arguments:

 `id`: could be of any type. Can be used to implement logics based on   numerical ids or to add descriptive informations about the load kind.
 
 e.g. `1` or `"poc1"`.

##### **Attributes**

All the arguments of the `__init__`.

`power_history`: a list containing all values of the grid power in `kW`. It gets filled during the simulation.

##### **Class Attributes**

- `all_grids`: list containing all instances of the class.

##### **Class Methods**

- `getAllGrids(cls)`: returns a list of all instances of the class.

##### **Instance Methods**

- `withdraw(self, power_value)`: a method that represents withdrawing power from a grid instance.
 

- `inject(self, power_value)`: a method that represents injecting power from a grid instance.
 
- `update(cls)`: a method that updates the instance `power_history` attribute if unchanged by the user defined logic.