#!/usr/bin/env python3

'''
GoPro-Concat-Automation  v 0.1
March 2019
created by: steven cucolo stevenc.github@gmail.com

GoPro records MP4 files that are segmented based on a 4Gb file size limit.
This script will go through a large batch of segmented GoPro files and
merge them based on their GoPro file number and creation dates.
An option to downconvert the merged file is also provided. The file merge
and downconvert is performed by FFMPEG.
'''

import gopro_concat as gp


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
        DownConvert (Y/N):    {str(down_convert)} \n \
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

