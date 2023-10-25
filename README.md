# rpitx-expansion-board

Expansion board for **Raspberry Pi 4 Model B** allowing to use coaxial SMA output and switchable filters instead of direct wire connection of radio equipment (antennas, amplifiers, switches, etc.) to GPIO during working with the [rpitx][2] or [rpitx-ui][3] package.

The PCB is installed by attaching to the GPIO of the Raspberry Pi and can be additionally fixed by using the holes on the Raspberry Pi and expansion board side.

## Current development progress:
[![Progress](https://img.shields.io/badge/rpitx--expansion--board-not%20tested-red.svg?longCache=true&style=for-the-badge)](https://easyeda.com/IgrikXD/rpitx-expansion-board)&nbsp;[![Progress](https://img.shields.io/badge/app%20version-0.2-blue.svg?longCache=true&style=for-the-badge)](./ControlApplication)&nbsp;[![Progress](https://img.shields.io/badge/pcb%20version-0.0-blue.svg?longCache=true&style=for-the-badge)](./EasyEDA)

## Application usage:
The **_rpitx-control_** application is used to control the expansion board.

## PCB implementations at EasyEDA platform:
- [rpitx-expansion-board][1] ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))

## How to use this repository?
In [Datasheets](./Datasheets) and [Schematics](./Schematics) directories, you can find all necessary technical documentation for the used components and schematic files in PDF format. If you only need GERBER files, you can find them in the appropriate [Gerbers](./Gerbers) directory. In the [EasyEDA](./EasyEDA) directory, you can find a list of files for implementing the ready device (files can be imported into EasyEDA editor). Based on submitted files, you can order PCB from factory manufacturing make the device independently.

## Basic device characteristics:
**PCB versions:**
* **rpitx-expansion-board-SP3T** - PCB with 3 switchable filters.  
* **rpitx-expansion-board-SP4T** - PCB with 4 switchable filters.  
* **rpitx-expansion-board-SP6T** - PCB with 6 switchable filters.  
* **rpitx-expansion-board-SP3T-LNA** - PCB with 3 switchable filters and LNA.  
* **rpitx-expansion-board-SP4T-LNA** - PCB with 4 switchable filters and LNA.  
* **rpitx-expansion-board-SP6T-LNA** - PCB with 6 switchable filters and LNA.  

**RF connector:** SMA  
**Feed line:** 50 Ohm coaxial cable  
**Used PCB Material:** FR-4  
**PCB thickness:** 1.6 mm  
**PCB copper weight:** 1 oz  

## Resources:
[rpitx project page at GitHub][2]  
[rpitx-ui project page at GitHub][3]  
[Buy filters][4] / [amplifiers][5] / [RF switches][6]  

## How to contact me?
- E-mail: igor.nikolaevich.96@gmail.com
- Telegram: https://t.me/igrikxd
- LinkedIn: https://www.linkedin.com/in/igor-yatsevich/

  [1]: https://easyeda.com/IgrikXD/rpitx-expansion-board
  [2]: https://github.com/F5OEO/rpitx
  [3]: https://github.com/IgrikXD/rpitx-ui
  [4]: https://www.minicircuits.com/WebStore/RF-Filters.html
  [5]: https://www.minicircuits.com/WebStore/Amplifiers.html
  [6]: https://www.minicircuits.com/WebStore/Switches.html
