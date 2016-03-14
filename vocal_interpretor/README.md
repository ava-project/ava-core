Vocal Interpretor
========

This is the Vocal Interpretor part of the core.

##Build instructions (Linux)

###Dependencies
Make sure to install pocketsphinx.

---

###Compile
Once you have installed all dependencies, you need to compile the application:

```bash
# Compile
make

# Export the LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/lib

# Have fun!
./test -infile samples/list_current.wav
