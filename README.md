# Ai-Media-Guardian 🎬

This project provides a Micro Command Protocol (MCP) server for controlling a VLC media player instance. 🕹️ It allows you to interact with VLC through a simple, text-based interface, making it suitable for automation and integration with other systems.

## Features ✨

*   **Remote Control:** Control VLC playback (play ▶️, pause ⏸️, stop ⏹️, seek) remotely.
*   **Volume Control:** Adjust the volume 🔊 and mute/unmute 🔇 VLC.
*   **Status Monitoring:** Retrieve the current status of the VLC player (playing, paused, title, etc.). ℹ️
*   **Video Settings:** Adjust video brightness 🔆, aspect ratio, and crop.
*   **Audio Settings:** Adjust playback rate ⏩ and select audio devices.
*   **Snapshot:** Take snapshots of the current video frame. 📸
*   **MCP Interface:** Communicates using the Micro Command Protocol (MCP), allowing for easy integration. 🤝

## Prerequisites ⚙️

*   **VLC Media Player:** VLC must be installed on your system. 💻
*   **Python:** Python 3.6 or higher is required. 🐍
*   **Python Packages:** The following Python packages are required:
    *   `mcp`
    *   `requests`
    *   `urllib3`
    *   `socket`

## Installation 🚀

1.  **Clone the repository:**

    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Create a `requirements.txt` file containing `mcp`, `requests`, `urllib3`)*

## Configuration 🛠️

Edit the `settings.py` file to configure the following settings:

*   `VLC_PATH`: The path to the VLC executable.
*   `VLC_HOST`: The hostname or IP address where the VLC HTTP interface is running.  Defaults to `http://localhost`.
*   `VLC_PORT`: The port number of the VLC HTTP interface. Defaults to `8080`.
*   `VLC_PASSWORD`: The password used to access the VLC HTTP interface. 🔑
*   `VLC_STARTUP_WAIT`: The time (in seconds) to wait for VLC to start before sending commands.

## Usage 💡

1.  **Start the MCP server:**

    ```bash
    python src/mcp_server.py
    ```

    This will start the MCP server, which listens for commands on the standard input (stdio).

2.  **Interact with the server:**

    You can use an MCP client to send commands to the server.  For example:

    ```
    tool launch_vlc
    tool load_video /path/to/your/video.mp4
    tool play
    tool pause
    tool status
    tool shutdown_vlc
    ```

## Project Structure 📂

*   `src/mcp_server.py`: The main MCP server script.
*   `src/vlc_controller.py`:  Contains the low-level VLC control logic.
*   `settings.py`: Configuration file for VLC settings.
*   `requirements.txt`: Lists the Python package dependencies.
*   `README.md`: This file. 📝

## Contributing 🤝

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License 📜

[License information here - e.g., MIT License]