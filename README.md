# Lightweight DNS Server

## Overview

This project implements a lightweight DNS server using Python. It supports basic DNS query handling along with secure client-server communication and a GUI interface.

## Features

* Custom DNS resolution
* Lightweight UDP-based server
* Secure client communication
* GUI for user interaction

## Project Structure

* `server.py` → DNS server implementation
* `client.py` → Basic client
* `secure_client.py` → Secure client
* `secure_control_server.py` → Security control layer
* `GUI.py` → Graphical interface

## How to Run

### Start Server

```
python server.py
```

### Run Client

```
python client.py
```

### Run GUI

```
python GUI.py
```

## Requirements

* Python 3.x

## Future Improvements

* Caching support
* Load balancing
* Advanced security features
