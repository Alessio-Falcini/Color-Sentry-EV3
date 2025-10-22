# Color-Sentry-EV3: High-Performance Client-Server Robotics System

> A real-time, **bi-directional Client-Server** system developed for the **LEGO Mindstorms EV3** platform, utilizing **TCP/IP Sockets**. The **EV3 (Pybricks Server)** acts as a digital sentry, streaming **real-time color readings** from its sensor. The **Desktop GUI (Python/Tkinter Client)** provides visualization, user control, and the capability to transmit **remote motor control commands** back to the robot.

***

## 1. Project Overview and Rationale

This project was developed as a laboratory exercise to demonstrate the implementation of a robust, low-latency communication model within a robotics context. It successfully bridges the gap between the embedded environment of the EV3 and a feature-rich desktop application, focusing on network-enabled remote control and sensing capabilities.

## 2. Core Architecture: TCP/IP Client-Server Model

The system operates based on a strict two-component TCP/IP architecture, ensuring modularity and clear separation of concerns. The communication is established over a local network (e.g., Wi-Fi or USB tethering), with the EV3 listening on **Port 12345** (as defined in `ev3-server/main.py`).

### 2.1. Server Component (EV3)

The EV3 Brick runs the server application, built using **Pybricks (Micropython)**.

* **Role:** Data acquisition (Color Sensor on Port S1) and actuation (Motor control on Port D).
* **Mechanism:** Initializes a **Socket Server** and manages the continuous communication loop.
* **Operation:**
    **Data Stream (EV3 $\rightarrow$ Client):** Reads the current color and transmits the color name as a string in real-time.
    **Command Stream (Client $\rightarrow$ EV3):** Receives discrete commands (e.g., `START_MOTOR`, `STOP_MOTOR`) and executes them via the Motor device interface.

### 2.2. Client Component (PC)

The Client application runs on a standard PC.

* **Role:** User Interface, real-time data visualization, and remote command transmitter.
* **Interface:** Built with **Python's Tkinter** (included in standard Python 3) for the framework and **Pillow (PIL)** for custom graphics and visual theme implementation.
* **Mechanism:** Establishes a **Socket Client** connection to the EV3's IP address. It utilizes **threading** to process continuous socket data reception without interrupting the main Graphical User Interface (GUI) thread.

## 3. Project Structure

The repository is organized to clearly separate the platform-specific codebases and documentation.

| Path | Type | Content and Purpose |
| :--- | :--- | :--- |
| **`Color-Sentry-EV3/`** | Repository Root | The main project directory. |
| ├── **`client/`** | Folder | Contains the code for the **Client** application on the PC (Graphical User Interface). |
| │   ├── `gui_colori.py` | Python File | The main GUI in **Tkinter** and the logic for managing the **Socket Client**. |
| │   └── `requirements.txt` | Text File | List of Python libraries required for the client (e.g., `Pillow`). |
| ├── **`ev3-server/`** | Folder | Contains the code for the **Server** application running on the EV3 robot. |
| │   └── `main.py` | Python File | The core **Pybricks** code for the EV3: sensor initialization, motor control, and **Socket Server** logic. |
| ├── **`docs/`** | Folder | Contains in-depth project documentation. |
| │   └── `Tesi d'Informatica LegoEV3.pdf` | Document | The complete thesis or project report, containing architectural analysis and results. |
| ├── `.gitignore` | Configuration | Instructs Git which temporary files and directories (`__pycache__`, system files, etc.) to ignore during commits. |
| └── `LICENSE` | License | Contains the terms of the **MIT License**, defining how the code may be used and distributed by others. |
## 4. Setup and Execution Instructions

### 4.1. Hardware and Software Prerequisites

* **Hardware:** LEGO Mindstorms EV3 Brick, EV3 Color Sensor (Port S1), EV3 Large Motor (Port D).
* **Software (EV3):** EV3 Brick running **Pybricks/Micropython**.
* **Software (PC):** PC with Python 3.x installed.

### 4.2. EV3 Server Initialization

1.  **Code Transfer:** Upload the file located at `ev3-server/main.py` onto your EV3 brick.
2.  **Network Configuration:** Ensure the EV3 is on the same local network as the Client PC and note its specific **IP Address**.
3.  **Execution:** Run `main.py` on the EV3. The server will initialize and await a client connection on **Port 12345**.

### 4.3. PC Client Initialization

### 4.3. PC Client Initialization

1.  **Dependencies:** This project requires Python 3.x dependencies for the Graphical User Interface (GUI). Install the necessary libraries listed in `requirements.txt`:
    ```bash
    pip install -r client/requirements.txt
    ```
    *(Note: The primary external dependency is **Pillow (PIL)** for handling graphical assets, while Tkinter is included in standard Python 3 distributions.)*

2.  **Configuration:** Crucially, update the **`SERVER_IP`** variable within the file **`client/gui_colori.py`** to match the **IP Address** of your EV3 Brick on the network.

3.  **Execution:** Launch the application from your command-line interface (CLI):
    ```bash
    python client/gui_colori.py
    ```

4.  **Operation:** Use the dedicated buttons within the GUI to initiate the socket connection, observe the real-time color stream, and transmit motor control commands remotely to the EV3 server.

## 5. Documentation and License

* **Detailed Thesis:** A complete technical analysis, including communication protocols, implementation details, and performance results, is available in the `docs` folder.
* **License:** This project is licensed under the **MIT License**. Refer to the [LICENSE](LICENSE) file for complete usage and redistribution terms.
