# -----------------------------------------------------------
# Changelog:
# -----------------------------------------------------------
# Version 0.5: 
# -----------------------------------------------------------
# Handling the situation when the filter is not installed
# Now, you can tell the program that the filter is not installed 
# on the PCB. What is it for? For example, you are using the 
# rpitx-expansion-board-SP6T board but have soldered only 3 
# filters out of 6 since you simply do not need the remaining 
# filters - to highlight that the filters are not installed on 
# the PCB, you can select the <Not installed> item when selecting 
# the case type for a specific filter. In this case, the RF 
# path for this filter will be excluded from the activation 
# list, and in the main menu of the application, you will see 
# only those filters that are available for activation.
# The changes also affected the display of information about 
# the active expansion board. Now, if the filter is not installed, 
# you will see the corresponding information.
# -----------------------------------------------------------
# Version 0.4: 
# -----------------------------------------------------------
# Adding the ability to install an application on the system
# Added setup.py file containing information about the 
# ControlApplication package and allowing you to install the 
# application on the system using pipx. It is recommended to 
# install application using pipx, in which case the application 
# will be installed in an isolated environment and will not 
# affect packages already installed on the system.
# 
# Handling the situation of missing CONFIGS_DIR directory
# Now, if the CONFIGS_DIR directory does not exist, when you 
# try to load the device configuration, an error message is 
# displayed after which you return to the main application menu.
# Previously, such an action would cause an exception and crash 
# the application.
# 
# Displaying information about GPIO ports simulation mode
# If IS_MOCK_GPIO_USED = True is set, when the application starts, 
# an information message will be displayed stating that GPIO ports 
# simulation is being used. The state of the actual GPIO ports 
# will not be changed during application execution. This mode is 
# used only for debugging the application on devices other than 
# Raspberry Pi.
    
# Changing the configuration creation process
# Now, if you accidentally select an incorrect component case, 
# you can go back a step by clicking the Cancel button and select 
# the component case again. If you click the Cancel button in the 
# component case selection menu, the creation of the device 
# configuration will be aborted and you will be returned to the 
# main menu.
# Previously, when you clicked the Cancel button, regardless of 
# whether you were selecting a component case or a specific 
# component model, configuration creation was aborted and you 
# were returned to the main menu.
# 
# Avoiding the use of application startup arguments
# Application startup arguments are no longer used as this 
# approach is incompatible when using entry_points in setup.py. 
# entry_points initiates the launch of a specific function 
# specified in its parameters. With this launch model, sys.argv 
# contains only the name of the script to be launched; any 
# additional arguments passed are ignored!
# 
# Now, to enable debug mode (launch argument --show-debug-info), 
# before installing the application, you need to run the following 
# command, which will set the variable SHOW_DEBUG_INFO = True and 
# activate debug mode:
# sed -i 's/SHOW_DEBUG_INFO = False/SHOW_DEBUG_INFO = True/' ControlApplication/main.py
# 
# To use MockFactory to simulate GPIO ports (launch argument 
# --use-mock-gpio), before installing the application you need to 
# run a command that will set the variable IS_MOCK_GPIO_USED = True 
# and enable GPIO ports simulation:
# sed -i 's/IS_MOCK_GPIO_USED = False/IS_MOCK_GPIO_USED = True/' ControlApplication/main.py
# 
# The --help argument is no longer processed by any alternative 
# methods.
# 
# Changing the module import process
# Modules are now imported relative to the ControlApplication 
# package name. This is necessary for the application to work 
# correctly after installation.
# 
# Updating the main README.md file
# Updating information about the application installation and 
# uninstallation process.

# Updating .gitignore
# Excluding directories related to the application installation 
# process.

# Codebase refactoring
# -----------------------------------------------------------
# Version 0.3: 
# -----------------------------------------------------------
# The FiltersList and AmplifiersList directories have been 
# moved to the ControlApplication directory. Now, dumps of 
# components and configurations of expansion boards are saved 
# taking into account the parent directory in which the 
# application source files are located.
# 
# The application execution order has been changed. Now, when 
# you start the program, you are asked to choose one of two 
# possible actions: creating a new device configuration or 
# loading an existing one.
# When creating a new configuration, you are prompted to 
# select the type of device for which the configuration is 
# being created.
# When loading an existing configuration, you are prompted to 
# select a configuration file from the list (the board type is 
# determined automatically). If the application does not find 
# information about saved configurations, an information message 
# is displayed, after which you will be returned to the main menu.
# 
# Checking for the presence of .csv files of component models
# When the program starts, it checks whether .csv files exist in 
# the FiltersList and AmplifiersList directories. These files are
# used to build a list of available components when creating a 
# device configuration. If it is not possible to load the 
# previously created .pkl dump of the list of components and the 
# necessary .csv files to build the list of components are 
# missing, an error message is displayed in the console and the 
# program ends.
# 
# Code refactoring.
# -----------------------------------------------------------
# Version 0.2: 
# -----------------------------------------------------------
# When the activateRFPath() function is called, 
# the activateRFOutput() function is called on a separate 
# thread for each of the RFSwitch objects. This eliminates 
# the problem of sequential switching of GPIO states for each 
# of the RFSwitch objects - first the input switch was switched, 
# then the output switch. Now, we switch the states of two 
# switches simultaneously.
# 
# The ComponentsList constructors are now called in separate 
# threads, which allows reading data about filters and 
# amplifiers in parallel rather than sequentially.
# When creating a ComponentsList object, each of the .csv files 
# is now processed in a separate thread.
# 
# Added highlighting of application start and stop timestamp 
# using '-' signs.
# 
# whiptail_interface.msgbox() is now called with an additional 
# --scrolltext parameter
# -----------------------------------------------------------