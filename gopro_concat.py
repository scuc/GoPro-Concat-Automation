
#!/usr/bin/env python3

'''
GoPro-Concat-Automation  v 0.2
March 2019

Concat Steps:
    Make a list of all the files in a GoPro a directory.
    Loop through the list and group files based on name and creation.
    Get the mediainfo for these files.
    Create a .txt file(s) with the full paths of files used for sub to FFMPEG.
    FFMPEG concats the grouped MP4 into one file, and gives the option to
    downconvert.
'''

import inspect
import logging
import os
import re
import subprocess
import sys
import time

import get_mediainfo as media

from datetime import datetime
from pathlib import Path
from operator import itemgetter
from pymediainfo import MediaInfo
from time import localtime, strftime


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

    down_convert = str(input("Downconvert the GoPro files to 10Mbit [Yes/No]: "))

    while True:
        if down_convert.lower() == 'yes':
            down_convert = True
            break
        elif down_convert.lower() == 'no':
            down_convert = False
            break
        else:
            print(f"{down_convert} is not a valid choice.")
            down_convert = str(input("Please select Yes or No (Y/N): "))
            continue

    return [source_path, output_path, down_convert]

def get_gopro_list(source_path):
    '''
    Create a list of all the MP4 files in the given Source Dir.
    File names must follow the specific pattern defined in the
    regex statement.
    '''
    os.chdir(source_path)

    gopr_source_list = []
    gopr_key_list = []
    gopr_dict = {}

    file_list = sorted(os.listdir(source_path), key=os.path.getctime)

    # print("FILE LIST: " + str(file_list))

    for gopro_file in file_list:
        if gopro_file.endswith('.MP4'):
            gopr_source_list.append(gopro_file)
        else:
            continue

    print("GoPRO SRC LIST: " + str(gopr_source_list))

    for file in gopr_source_list:
        print("FILE: " + file)
        regex = r"(GOPR\d{4})\."
        gp = re.search(regex, file)
        # print(gp)
        if gp is not None:
            gopr_key_list.append(file)
        else:
            pass

    print("GP KEY LIST: " + str(gopr_key_list))

    for file in gopr_key_list:
        filenum = file[4:]
        fstring = f"(GP\\d{{2}}{filenum})"
        r = re.compile(fstring)
        gplist = list(filter(r.match, gopr_source_list))
        gplist.insert(0,file)
        gopr_dict.update({file:gplist})


    print(gopr_dict)
    return gopr_dict


def create_datetime(encoded_date):
    '''
    Create datetime string values based on the encoded_time value
    contained in the mediainfo for a MP4 file.
    '''

    year = int(encoded_date[4:8])
    month = int(encoded_date[9:11])
    day = int(encoded_date[12:14])
    hour = int(encoded_date[15:17])
    minute = int(encoded_date[18:20])
    second = int(encoded_date[21:23])

    gp_datetime = datetime(year, month, day, hour, minute, second)
    creation_date_str = gp_datetime.strftime("%Y%m%d%H%M%S")

    # print(gp_datetime)
    # print(creation_date_str)

    return creation_date_str


def create_ffmpeg_txtfiles(gprkey, gopr_dict, source_path, output_path):

    '''
    create a txt file with paths to a set our MP4 source files.
    the text file is passed into the FFMEG statment as the input.
    file '/path/to/file1'
    file '/path/to/file2'
    file '/path/to/file3'
    '''
    gpr_txt_path = Path(output_path + gprkey[:-4] + '.txt')

    if gpr_txt_path.exists() is True:
        pass
        print("PASS on TXT FILE")
    else:
        gpr_sources_txt = open(gpr_txt_path, 'a')

        # print("GPR TXT PATH: " + str(gpr_txt_path))

        gprfile_list = sorted(gopr_dict[gprkey])

        for file in gprfile_list:
            file_stmnt = "file " + '\'' + source_path + file + '\'' + "\n"
            gpr_sources_txt.write(file_stmnt)

            # print("FILE STMNT: " + file_stmnt)

        gpr_sources_txt.close()

    return gpr_txt_path


def ffmpeg_concat(gprkey, gopr_dict, source_path, output_path):
    '''
    Use FFMPEG subprocess call to merge a set of MP4 files.
    '''
    os.chdir(output_path)

    gpr_txt_path = create_ffmpeg_txtfiles(gprkey, gopr_dict, source_path,
        output_path)

    mediainfo = media.get_mediainfo(source_path, gprkey)

    print("MEDIA INFO: " + str(mediainfo))

    encoded_date = mediainfo['v_encoded_date']

    gprkey_date = create_datetime(encoded_date)
    creation_time = 'creation_time=' + encoded_date[4:]

    print("CREATION TIME: " + creation_time)

    mp4_output = str(gprkey[:-4]) + '_' + gprkey_date[:-6] + '.MP4'

    ffmpeg_cmd = [
                  'ffmpeg', '-safe', '0', '-f', 'concat',  '-i',
                  gpr_txt_path, '-c', 'copy', '-metadata', creation_time,
                  mp4_output
                  ]

    output_log = open(output_path + '/' + gprkey[:-4] + '_output.log', 'a')

    sp = subprocess.Popen(ffmpeg_cmd,
                          shell=False,
                          stderr=output_log,
                          stdout=output_log)

    stdout, stderr = sp.communicate(input='N')

    output_log.close()

    return mp4_output, mediainfo, creation_time


def ffmpeg_downconvert(gprkey, gopr_dict, source_path, output_path):
    '''
    Use a FFMPEG subprocess call to downconvert a merged MP4 file.
    '''
    os.chdir(output_path)

    mp4_output, mediainfo, creation_time = ffmpeg_concat(gprkey, gopr_dict, source_path, output_path)

    bitrate = mediainfo['v_bit_rate']
    bitratemode = mediainfo['v_bit_rate_mode']
    codec = mediainfo['v_codec_id']
    framerate = mediainfo['v_frame_rate']
    encoded_date = mediainfo['v_encoded_date']
    width = mediainfo['v_width']
    height = mediainfo['v_height']
    a_format = mediainfo['a_format'].lower()
    a_bitrate = mediainfo['a_bit_rate']

    video_siz = str(width) + 'x' + str(height)

    mp4_source = mp4_output
    mp4_output = output_path + mp4_source[:-4] + "_downconvert.mp4"

    print("MP4 SOURCE:" + str(mp4_source))
    print("MP4 OUTPUT:" + str(mp4_output))

    output_log = open(output_path + '/' + gprkey[:-4] + '_output.log', 'a')

    ffmpeg_cmd = ['ffmpeg', '-i', mp4_source, '-map', '0:0',
          '-map', '0:1', '-c:a', a_format, '-ab', '128k',
          '-strict', '-2', '-async', '1', '-c:v', 'libx264',
          '-b:v', '5000k', '-maxrate', '5000k', '-bufsize',
          '10000k', '-r', framerate, '-s', video_siz, '-aspect',
          '16:9', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
          '-level', '41', '-partitions',
          'partb8x8+partp4x4+partp8x8+parti8x8', '-b-pyramid',
          '2', '-weightb', '1', '-8x8dct', '1', '-fast-pskip',
          '1', '-direct-pred', '1', '-coder', 'ac', '-trellis',
          '1', '-me_method', 'hex', '-flags', '+loop',
          '-sws_flags', 'fast_bilinear', '-sc_threshold', '40',
          '-keyint_min', '60', '-g', '600', '-qmin', '3', '-qmax',
          '51', '-metadata', creation_time, '-sn', '-y', mp4_output]

    sp = subprocess.Popen(ffmpeg_cmd, shell=False,
                      stderr=output_log, stdout=output_log)

    (stderr, stdout) = sp.communicate(input='N')

    print(stderr, stdout)

    output_log.close()

    print("COMPLETE")
