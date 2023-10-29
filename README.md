# rpitx-expansion-board

Expansion board for **Raspberry Pi 4 Model B** that eliminates the need for a direct wired connection of radio equipment (such as antennas, amplifiers, switches, etc.) to GPIO when working with [rpitx][2] or [rpitx-ui][3] packages. Now, you can use coaxial SMA output, switchable filters, and built-in LNA.

The expansion board is installed by connecting it to the 40-pin Raspberry Pi header and can be fixed additionally by connecting holes on the Raspberry Pi and the expansion board.

## Current development progress:
[![Progress](https://img.shields.io/badge/rpitx--expansion--board-not%20tested-red.svg?longCache=true&style=for-the-badge)](https://easyeda.com/IgrikXD/rpitx-expansion-board)&nbsp;[![Progress](https://img.shields.io/badge/app%20version-0.2-blue.svg?longCache=true&style=for-the-badge)](./ControlApplication)&nbsp;[![Progress](https://img.shields.io/badge/pcb%20version-0.0-blue.svg?longCache=true&style=for-the-badge)](./EasyEDA)

## Application usage:
The **_rpitx-control_** application is used to control the expansion board.
```sh
sudo apt update
git clone https://github.com/IgrikXD/rpitx-expansion-board
pip3 install gpiozero pickle pandas
cd rpitx-expansion-board
python3 ./ControlApplication/main.py
```

## Current available implementations at EasyEDA platform:

### PCB without built-in LNA:
- [rpitx-expansion-board-SP3T][1] - Expansion board with **3** switchable filters ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))
- [rpitx-expansion-board-SP4T][1] - Expansion board with **4** switchable filters ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))
- [rpitx-expansion-board-SP6T][1] - Expansion board with **6** switchable filters ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))
### PCB with built-in LNA:
- [rpitx-expansion-board-SP3T-LNA][1] - Expansion board with **3** switchable filters and built-in LNA ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))
- [rpitx-expansion-board-SP4T-LNA][1] - Expansion board with **4** switchable filters and built-in LNA ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))
- [rpitx-expansion-board-SP6T-LNA][1] - Expansion board with **6** switchable filters and built-in LNA ([Components list](./Components-list.md), [Usage guide](./Usage-guide.md))


## How to use this repository?
In [Datasheets](./ExpansionBoards/Datasheets) and [Schematics](./ExpansionBoards/Schematics) directories, you can find all necessary technical documentation for the used components and schematic files in PDF format. If you only need GERBER files, you can find them in the appropriate [Gerbers](./ExpansionBoards/Gerbers) directory. In the [EasyEDA](./ExpansionBoards/EasyEDA) directory, you can find a list of files for implementing the ready device (files can be imported into EasyEDA editor). Based on submitted files, you can order PCB from factory manufacturing make the device independently.

## Basic device characteristics:
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
