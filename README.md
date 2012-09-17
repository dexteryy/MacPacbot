# MacPacbot

MacPacbot is a Python toolkit of PAC(auto proxy configuration) for Mac OS X, which makes it much easier to create, edit and enable PAC script.
It could transform a simple YAML config into a valid PAC script. 

## Install

    pip install MacPacbot

## Usage

Transform YAML info PAC:

    sudo pacbot <yaml_file> -o <pac_file>

Automatically detect network-service and update auto proxy configuration:

    sudo pacbot -u [-o <pac_file>]

Disable auto proxy in current network-service:

    sudo pacbot -s off

Vim plugin:
```vim
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
```
