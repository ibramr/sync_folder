#!/usr/bin/env python3

'''
Written by: Amr Ibrahim

Purpose: This script synchronizes two folders, namely source and replica,
         while maintaining an identical copy of source folder at replica folder. 
         Synchronization is performed periodically every 30 seconds and any creation/copying/removal
         operation of file in source folder is logged to sync_log.txt and console.

Usage: python mycode.py --source [path to source folder] --replica [path to replica folder, if not given, new one will be created] --log [path to logging file] --interval [synchronization interval, default is 5 seconds]
'''

import os
import sys
import time
import shutil
import logging
import argparse


# Define a the main function (sync_folder) to synchronize the folders
def sync_folder(source_folder, replica_folder, sync_interval):
        
    # Loop to synchronize the replica folder at the specified sync interval
    while True:
                    
        # Get a list of file in the source folder
        source_file = os.listdir(source_folder)
    
        # Iterate over the source files
        for file in source_file:
            
            # Get the full paths of the source and replica file
            source_path = os.path.join(source_folder, file)
            replica_path = os.path.join(replica_folder, file)
    
            # If the file exists in the source folder but not in the replica folder,
            # copy it to the replica folder, log and print the operation
            if os.path.isfile(source_path) and not os.path.exists(replica_path):
                shutil.copy2(source_path, replica_path)
                # Get the current date and time
                local_time = time.localtime(time.time())
                logging.info(f'Copied {file} from {source_folder} to {replica_folder}')
                date = time.strftime("%Y-%m-%d", local_time)
                current_time = time.strftime("%H:%M:%S", local_time)
                print(f'{date} {current_time}: Copied {file} from {source_folder} to {replica_folder}')
    
            # If the file exists in both the source folder and the replica folder,
            # compare their modification times. If the source file has been modified more recently,
            # copy it to the replica folder, log and print the operation
            elif os.path.isfile(source_path) and os.path.exists(replica_path):
                source_mtime = os.path.getmtime(source_path)
                replica_mtime = os.path.getmtime(replica_path)
                if source_mtime > replica_mtime:
                    shutil.copy2(source_path, replica_path)
                    local_time = time.localtime(time.time())
                    logging.info(f'Updated {file} in {replica_folder} to match {source_folder}')
                    date = time.strftime("%Y-%m-%d", local_time)
                    current_time = time.strftime("%H:%M:%S", local_time)
                    print(f'{date} {current_time}: Updated {file} in {replica_folder} to match {source_folder}')
    
        # Get a list of file in the replica folder
        replica_file = os.listdir(replica_folder)
    
        # Iterate over the replica files
        for file in replica_file:
            
            # Get the full paths of the source and replica file
            source_path = os.path.join(source_folder, file)
            replica_path = os.path.join(replica_folder, file)
    
            # If the file exists in the replica folder but not in the source folder,
            # delete it from the replica folder, log and print the operation
            if os.path.isfile(replica_path) and not os.path.exists(source_path):
                os.remove(replica_path)
                local_time = time.localtime(time.time())
                logging.info(f'Removed {file} from {replica_folder} to match {source_folder}')
                date = time.strftime("%Y-%m-%d", local_time)
                current_time = time.strftime("%H:%M:%S", local_time)
                print(f'{date} {current_time}: Removed {file} from {replica_folder} to match {source_folder}')
                
        # Sleep for the specified interval before looping again
        try:
            time.sleep(sync_interval)
        except:
            print('Aborting...')
            sys.exit()
        

if __name__ == '__main__':
    
    # Parse out the paths of source and replica folders, the path of log file, and the sync interval from the 
    # command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='', help='The path of the source folder')
    parser.add_argument('--replica', type=str, default='', help='The path of the replica folder')
    parser.add_argument('--log', type=str, default='log_file.txt', help='The path of the logging file')
    parser.add_argument('--interval', type=float, default='5', help='The synchronization interval in seconds')
    parser = parser.parse_args()
    
    # Set up the logger folder
    if not(os.path.exists(parser.source)):
        print('Source folder does not exist\nAborting...')
        sys.exit()
    else:
        source_folder = os.path.abspath(parser.source)
        print(f'Source folder is: {source_folder}')

    # Set up the replica folder
    if not(os.path.exists(parser.replica)):
        print('No replica folder was given...')
        answer = input('Would you like to create a replica folder? [y|n]:')
        if answer == 'n':
            print('Aborting...')
            sys.exit()
        elif answer == 'y':            
            replica_folder = source_folder + '_replica'
            if not(os.path.exists(replica_folder)):
                try:
                    os.mkdir(replica_folder)
                    print(f'Replica folder is: {replica_folder}')
                except:
                    print('Failed to create a replica folder...\nAborting...')
                    sys.exit()
    else:
        replica_folder = os.path.abspath(parser.replica)
        print(f'Replica folder is: {replica_folder}')

    # Set up the synchornization time 
    sync_interval = parser.interval
    print(f'Synchronization time will be set to {sync_interval} seconds')

    # Set up the logger file
    log_file = os.path.join(os.path.abspath(parser.log))
    if not(log_file.endswith('.txt')):
        log_file = log_file + '.txt'
    print(f'Operations will be logged to: {log_file}')
    logging.basicConfig(filename=log_file,  filemode='a', level=logging.INFO,
                        format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
    
    # Start the synchronization
    print('synchronization started...')
    sync_folder(source_folder, replica_folder, sync_interval)