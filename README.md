# Python Youtube Player
Python project to play Youtube videos through a multi-clint server and receive commands over the network 


## Description
This is a python project that uses both *pafy* and *vlc* libraries to stream videos from Youtube.

This project is final project for the class EE810 - Engineering Programming: Python at Stevens Institute of Technology.

## Features
* Multiclient - let everyone in the network add their music to your play-list
* Play-list Management - add, pause and skip any music on your play-list

## Usage
#### Dependencies
In order to run this project, you need to install both vlc and pafy. See the following links for installation guides:
* [Pafy Repository](https://github.com/mps-youtube/pafy)
* [VLC Bindings](https://wiki.videolan.org/Python_bindings/)

####Running the Server

```bash
usage: python server.py [hostname] [port]
example: python server.py localhost 9999```
