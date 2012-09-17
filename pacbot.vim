" vim plugin for pacbot

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

