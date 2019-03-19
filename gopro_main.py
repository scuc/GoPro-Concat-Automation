#!/usr/bin/env python3


import gopro_concat as gp


# set the global varibales for the script.

def gopro_main():

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

    if down_convert == False:
        gp.ffmpeg_concat(gopro_dict, source_path, output_path)
        print('Processing concat now...')

    else:
        ffmpeg_downconvert = gp.ffmpeg_downconvert(gopro_dict, source_path, output_path)

        print( "Processing downconvert now...")

    print('FFMPEG process complete.')

gopro_main()

