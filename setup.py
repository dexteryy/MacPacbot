#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

setup(
    name = 'MacPacbot',
    version = '1.0.6',
    author = 'dexteryy',
    author_email = 'dexter.yy@gmail.com',
    url = 'http://dexteryy.github.com/MacPacbot',
    description = 'MacPacbot is a Python toolkit of PAC(auto proxy configuration) for Mac OS X',
    entry_points = {
        "console_scripts": ['pacbot = MacPacbot.pacbot:main']
    },
    packages = ['MacPacbot'],
    keywords = ["PAC", "proxy", "mac", "GFW"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: System :: Systems Administration"
    ],
    long_description = """\
MacPacbot is a Python toolkit of PAC(auto proxy configuration) for Mac OS X, which makes it much easier to create, edit and enable PAC script.
It could transform a simple YAML config into a valid PAC script. 

## Usage

Transform YAML info PAC:

    sudo pacbot <yaml_file> -o <pac_file>

Automatically detect network-service and update auto proxy configuration:

    sudo pacbot -u [-o <pac_file>]

Disable auto proxy in current network-service:

    sudo pacbot -s off

Vim plugin:

    function! EnablePAC()
        if &filetype == 'javascript'
            !sudo pacbot -u -o %
        elseif &filetype == 'yaml'
            !sudo pacbot %
        endif
    endfunction

    command! PACenable call EnablePAC() 
    autocmd! bufwritepost *.pac :PACenable
    autocmd! bufwritepost *.ypac :PACenable

"""
)
