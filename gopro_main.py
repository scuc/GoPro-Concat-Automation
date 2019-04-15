#!/usr/bin/env python3

'''
GoPro-Concat-Automation  v 0.2
April 2019
created by: steven cucolo stevenc.github@gmail.com

GoPro records MP4 files that are segmented based on a 4Gb file size limit.
This script will go through a large batch of segmented GoPro files and
merge them based on their GoPro file number and creation dates.
An option to auto rotate and downconvert the merged file is also provided.
The file processing is performed by FFMPEG.
'''

import gopro_automate as gp


def print_intro():
    '''
    Get the user input for starting values (Source, Output, Downcovert)
    and begin the concat process.
    '''
    open_msg = f"\n\
    ================================================================\n \
                GoPro Automation Script, version 0.2 \n \
    This script will take a collection of chaptered GoPro video files \n \
    and stitch them together with the option to also downconvert them \n \
    to a 10Mbit file. \n \
    ================================================================\n"

    print(open_msg)

    source_path = str(input("Source path: "))

    output_path = str(input("Output path: "))

    down_convert = str(input("Downconvert the GoPro files [y/N]: "))

    auto_rotate = str(input("Allow FFMPEG to auto rotate video? [Y/n]: "))

    while True:
        if down_convert[0].lower() == 'y':
            down_convert = True
            break
        elif down_convert[0].lower() == 'n' or None:
            down_convert = False
            break
        else:
            print(f"{down_convert} is not a valid choice.")
            down_convert = str(input("Please select Yes or No [y/N] "))
            continue

    while True:
        if auto_rotate[0].lower() == 'y' or None:
            auto_rotate = True
            break
        elif auto_rotate[0].lower() == 'n':
            auto_rotate = False
            break
        else:
            print(f"{auto_rotate} is not a valid choice.")
            auto_rotate = str(input("Please select Yes or No [Y/n]: "))
            continue

    return [source_path, output_path, down_convert, auto_rotate]

def gopro_main():
    '''
    Get the user input and pass it into the concat and/or downconvert
    functions.
    '''
    gp_vars = gp.print_intro()

    source_path = gp_vars[0]
    output_path = gp_vars[1]
    down_convert = gp_vars[2]

    start_message = f"\
    ================================================================\n \
        Starting the GoPro concat with these values : \n \
        Source Path:   {str(source_path)} \n \
        Output Path:   {str(output_path)} \n \
        DownConvert:    {str(down_convert)} \n \
        Auto Rotation:    {str(down_convert)} \n \
    ===========================================================\n "

    print(start_message)

    gopro_dict = gp.get_gopro_list(source_path)
    gprkey_list = list(gopro_dict.keys())

    if down_convert == False:

        for gprkey in gprkey_list:
            gp.ffmpeg_concat(gopro_dict, source_path, output_path)
            print('Processing concat now...')

    else:

        for gprkey in gprkey_list:
            ffmpeg_downconvert = gp.ffmpeg_downconvert(gprkey, gopro_dict, source_path, output_path)

        print( "Processing downconvert now...")

    print('FFMPEG process complete.')

gopro_main()

