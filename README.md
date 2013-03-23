This script is for the times when you want to collect consecutive
screenshots and bunch them together in a directory.

You use the script by modifying the configuration variables to match
your environment (defaults to OS X), running it from the command-line
with one string argument.

Example:

    python screenies.py "my_tutorial"

Until you stop the script with Control-C, any new "Screen Shot ###.png"
files will be renamed and placed in a directory with the provided name.

    "~/Desktop/my_tutorial/my_tutorial1.png"
    "~/Desktop/my_tutorial/my_tutorial2.png"