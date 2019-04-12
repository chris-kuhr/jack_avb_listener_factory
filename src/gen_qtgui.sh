#!/bin/bash
pyuic5 qt/mainWindow.ui -o qtavdecc_listener_factory.py
pyuic5 qt/qtpacket_capture.ui -o qtpacket_capture.py
pyuic5 qt/qtpreferences.ui -o qtpreferences.py
