About
-------------------------------
MacPacbot is a Python toolkit for PAC(auto proxy configuration) of Mac OS X, which makes it much easier to create, edit and enable PAC script.
It could transform a simple YAML config into a valid PAC script. 

Usage
-------------------------------
Transform YAML info PAC:
`python pacbot.py <yaml_file> -o <pac_file>`

Automatically detect network-service and update auto proxy configuration:
`python pacbot.py -u [-o <pac_file>]`

Disable auto proxy in current network-service:
`python pacbot.py -s off`

