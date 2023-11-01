# rpitx-expansion-board

Expansion board for **Raspberry Pi 4 Model B** that eliminates the need for a direct wired connection of radio equipment (such as antennas, amplifiers, switches, etc.) to GPIO when working with [rpitx][1] or [rpitx-ui][2] packages. Now, you can use coaxial SMA output, switchable filters, and built-in LNA.

The expansion board is installed by connecting it to the 40-pin Raspberry Pi header and can be fixed additionally by connecting holes on the Raspberry Pi and the expansion board.

## Current development progress:
[![Progress](https://img.shields.io/badge/rpitx--expansion--board-not%20tested-red.svg?longCache=true&style=for-the-badge)](https://easyeda.com/IgrikXD/rpitx-expansion-board)&nbsp;[![Progress](https://img.shields.io/badge/app%20version-0.4-blue.svg?longCache=true&style=for-the-badge)](./ControlApplication)&nbsp;[![Progress](https://img.shields.io/badge/pcb%20version-0.0-blue.svg?longCache=true&style=for-the-badge)](./EasyEDA)

## Application usage:

Before building and installing the control application, you can perform the following steps (not required if you plan to use the application normally):

Enabling debugging mode (while the program is running, the log file APPLICATION_DIR/DebugInfo.log is created):
```sh
sed -i 's/SHOW_DEBUG_INFO = False/SHOW_DEBUG_INFO = True/' ControlApplication/main.py
```

Enabling the use of MockFactory to simulate GPIO ports (used to run and debug the application on non-Raspberry Pi devices):
```sh
sed -i 's/IS_MOCK_GPIO_USED = False/IS_MOCK_GPIO_USED = True/' ControlApplication/main.py
```

Installing and using **rpitx-control** application:
```sh
sudo apt update && sudo apt install git pipx
git clone https://github.com/IgrikXD/rpitx-expansion-board
cd rpitx-expansion-board
pipx ensurepath
pipx install .
rpitx-control
```

Uninstalling the rpitx-control application:
```sh
pipx uninstall rpitx-control
```

## Current available implementations at EasyEDA platform:
### Expansion boards without built-in LNA:
- [rpitx-expansion-board-SP3T][6] - Expansion board with **3** switchable filters ([Components list](./ExpansionBoards/rpitx-expansion-board-SP3T/Components-list.md), [Assembly guide](./ExpansionBoards/rpitx-expansion-board-SP3T/Assembly-guide.md), [Usage guide](./ExpansionBoards/rpitx-expansion-board-SP3T/Usage-guide.md))
- [rpitx-expansion-board-SP4T][7] - Expansion board with **4** switchable filters ([Components list](./ExpansionBoards/rpitx-expansion-board-SP4T/Components-list.md), [Assembly guide](./ExpansionBoards/rpitx-expansion-board-SP4T/Assembly-guide.md), [Usage guide](./ExpansionBoards/rpitx-expansion-board-SP3T/Usage-guide.md))
- [rpitx-expansion-board-SP6T][8] - Expansion board with **6** switchable filters ([Components list](./ExpansionBoards/rpitx-expansion-board-SP6T/Components-list.md), [Assembly guide](./ExpansionBoards/rpitx-expansion-board-SP6T/Assembly-guide.md), [Usage guide](./ExpansionBoards/rpitx-expansion-board-SP3T/Usage-guide.md))
### Expansion boards with built-in LNA:
- [rpitx-expansion-board-SP3T-LNA][9] - Expansion board with **3** switchable filters and built-in LNA ([Components list](./ExpansionBoards/rpitx-expansion-board-SP3T-LNA/Components-list.md), [Assembly guide](./ExpansionBoards/rpitx-expansion-board-SP3T-LNA/Assembly-guide.md), [Usage guide](./ExpansionBoards/rpitx-expansion-board-SP3T-LNA/Usage-guide.md))
- [rpitx-expansion-board-SP4T-LNA][10] - Expansion board with **4** switchable filters and built-in LNA ([Components list](./ExpansionBoards/rpitx-expansion-board-SP4T-LNA/Components-list.md), [Assembly guide](./ExpansionBoards/rpitx-expansion-board-SP4T-LNA/Assembly-guide.md), [Usage guide](./ExpansionBoards/rpitx-expansion-board-SP4T-LNA/Usage-guide.md))
- [rpitx-expansion-board-SP6T-LNA][11] - Expansion board with **6** switchable filters and built-in LNA ([Components list](./ExpansionBoards/rpitx-expansion-board-SP6T-LNA/Components-list.md), [Assembly guide](./ExpansionBoards/rpitx-expansion-board-SP6T-LNA/Assembly-guide.md), [Usage guide](./ExpansionBoards/rpitx-expansion-board-SP6T-LNA/Usage-guide.md))

## Basic characteristics of the expansion boards:
**RF connector:** SMA  
**Feed line:** 50 Ohm coaxial cable  
**Used PCB Material:** FR-4  
**PCB thickness:** 1.6 mm  
**PCB copper weight:** 1 oz 

## How to use this repository?
The [ControlApplication](./ControlApplication) directory contains the source code for the **rpitx-control** application. The [ExpansionBoards](./ExpansionBoards) directory contains information about all available expansion boards. After selecting a specific board in the [Datasheets](./ExpansionBoards/rpitx-expansion-board-SP3T/Datasheets) and [Schematics](./ExpansionBoards/rpitx-expansion-board-SP3T/Schematics) directories, you can find all the necessary technical documentation and schematic files in _.pdf_ format. If you only need _GERBER_ files, you can find them in the appropriate [Gerbers](./ExpansionBoards/rpitx-expansion-board-SP3T/Gerbers) directory. In the [EasyEDA](./ExpansionBoards/rpitx-expansion-board-SP3T/EasyEDA) directory, you can find a list of files for implementing the ready device (files can be imported into EasyEDA editor). Based on submitted files, you can order PCB from factory manufacturing make the device independently.  

Additionally, for each expansion board you can find a [list of required components](./ExpansionBoards/rpitx-expansion-board-SP3T/Components-list.md), [assembly guide](./ExpansionBoards/rpitx-expansion-board-SP3T/Assembly-guide.md) and an [example of use](./ExpansionBoards/rpitx-expansion-board-SP3T/Usage-guide.md) in conjunction with the **rpitx-control** application.

## Resources:
[rpitx project page at GitHub][1]  
[rpitx-ui project page at GitHub][2]  
[Buy filters][3] / [amplifiers][4] / [RF switches][5]  

## How to contact me?
- E-mail: igor.nikolaevich.96@gmail.com
- Telegram: https://t.me/igrikxd
- LinkedIn: https://www.linkedin.com/in/igor-yatsevich/

  [1]: https://github.com/F5OEO/rpitx
  [2]: https://github.com/IgrikXD/rpitx-ui
  [3]: https://www.minicircuits.com/WebStore/RF-Filters.html
  [4]: https://www.minicircuits.com/WebStore/Amplifiers.html
  [5]: https://www.minicircuits.com/WebStore/Switches.html
  [6]: https://easyeda.com/IgrikXD/rpitx-expansion-board-SP3T
  [7]: https://easyeda.com/IgrikXD/rpitx-expansion-board-SP4T
  [8]: https://easyeda.com/IgrikXD/rpitx-expansion-board-SP6T
  [9]: https://easyeda.com/IgrikXD/rpitx-expansion-board-SP3T-LNA
  [10]: https://easyeda.com/IgrikXD/rpitx-expansion-board-SP4T-LNA
  [11]: https://easyeda.com/IgrikXD/rpitx-expansion-board-SP6T-LNA
