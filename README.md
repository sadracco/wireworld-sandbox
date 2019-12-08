# wireworld_sandbox
Simple wireworld tool.

### What is wireworld?
Wireworld is a simple cellular automaton used to simulate logic circuits.  
Each cell can be in 4 different states:
- Empty
- Conductor
- Electron head
- Electron tail  

Simulation rules (every next generation each cell changes according to them):
- Empty -> empty
- Electron head -> electron tail
- Electron tail -> conductor
- Conductor -> electron head (if one or two neighbouring cells are electron heads)

### Better explanation
- [Wikipedia](https://en.wikipedia.org/wiki/Wireworld)
- [quinapalus.com](https://www.quinapalus.com/wires0.html)

### Requirements
- numpy `pip install numpy`
- pyqt5 `pip install pyqt5`

### Usage
- Extract the archive, make sure all required packages are installed and execute `window.py`
- Marker. Use **LMB** to place a wire. Click on wire with **RMB** to change it's state to electron head. Click on electron head with **RMB** to change its state to electron tail
- Eraser. Use **LMB** to remove a wire
- Broom. Clean an entire workspace
- Grid. Enable/disable background grid
- Pause. Start/stop the simulation
- Right arrow. One step of the simulation
- Up/Down arrow. Change speed of the simulation
- You can pan arround by moving your cursor while holding **MMB**
- Zoom in and out with **Scroll**

### Screenshots
![Example 1](/screenshots/screen1.png)
![Example 2](/screenshots/screen2.png)
