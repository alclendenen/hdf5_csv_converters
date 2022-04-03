# hdf5_csv_converters
Meant to be relatively simple program that takes in a h5 file from a gyroscope and outputs a csv with the measurements

The generic converter is a work in progress and the mobility lab one seems to be working along with a build that was target for Mac OS X

running mobility_lab_gyro_hdf5_to_csv_converter
- Make sure permissions on the file are open for the current user
- Make sure after you try and run it the first time on mac you go to System Preferences > Security & Privacy > General and you allow the program to run
- When you run the program you should get a terminal window along with a directory selection pop up
- Select the directory with the .h5 files you want to parse and the first half of the program will parse them and write them to a raw_data.csv file in the same directory of the .h5 files 
- Another dialog should pop up and if you want to further process the data you will need to select a .json file that specifies what files you want to process and the start and end times the data should be trimmed to. An example json is check in along side the build.
- Once processed the program will write to a processed_data.csv file and that is the end of the program.

notes:
- keep an eye on the terminal window as it will try and report things that went wrong
- The names of the output csv files do not change so if you run it more than once it will write over the old data in those files. So in order to not lose progress, you should rename the output files right after.
