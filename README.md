# MacPacbot

MacPacbot is a Python toolkit of PAC(auto proxy configuration) for Mac OS X, which makes it much easier to create, edit and enable PAC script.
It could transform a simple YAML config into a valid PAC script. 

## Install

    pip install MacPacbot

## Usage

Transform YAML info PAC, automatically detect network-service and update auto proxy configuration:

    sudo pacbot <yaml_file> [-o <pac_file>]

Update auto proxy configuration with an existing PAC file:

    sudo pacbot -u <pac_file>

Disable auto proxy in current network-service:

    sudo pacbot -s off

Vim plugin:
```vim
    function! EnablePAC()
        if &filetype == 'javascript'
            !sudo pacbot -u %
        elseif &filetype == 'yaml'
            !sudo pacbot %
        endif
    endfunction

    command! PACenable call EnablePAC() 
    autocmd! bufwritepost *.pac :PACenable
    autocmd! bufwritepost *.ypac :PACenable
```
