# gcode_previewer

This is a tool that creates jpg from a gcode. 
The idea was, that my older gcodes did not contain preview thumbnails.
Simply use
> for i in *gcode ; do python _layerd_preview.py $i ; done

in a bash environment and all files in this directory will be converted.
