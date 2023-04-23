# sync_folder
In this repository, a python script was created to synchronizes two folders, namely source and replica, while maintaining an identical copy of source folder at replica folder. Synchronization is performed periodically and any creation/copying/removal operation of file in source folder is logged and printed in console.

# Test
To run the code, open a terminal and paste the following command witht the right arguments:
'''
python mycode.py --source [path to source folder] --replica [path to replica folder, if not given, new one will be created] --log [path to logging file, if not given, log_file.txt will be created] --interval [synchronization interval, default is 5 seconds]
'''
