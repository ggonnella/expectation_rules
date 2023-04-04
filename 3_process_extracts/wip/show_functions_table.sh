grep -n -P ^U *.egc | grep function | sort -k4,6 | cattsv.rb -c 190 | less
