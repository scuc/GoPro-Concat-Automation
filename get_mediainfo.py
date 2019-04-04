#!/usr/bin/env python3

from pymediainfo import MediaInfo

file = "/Users/stevenc/Desktop/GOPRO/GOPR6344.MP4"

media_info = MediaInfo.parse(file)

media_dict = {}

for track in media_info.tracks:
    if track.track_type == 'Video':
        media_dict.update(v_format = track.format)
        media_dict.update(v_info = track.format_info)
        media_dict.update(v_profile = track.format_profile)
        media_dict.update(v_settings = track.format_settings)
        media_dict.update(v_settings_cabac = track.format_settings_cabac)
        media_dict.update(v_settings_reframes = track.format_settings_reframes)
        media_dict.update(v_format_settings_gop = track.format_settings_gop)
        media_dict.update(v_codec_id = track.codec_id)
        media_dict.update(v_codec_id_info = track.codec_id_info)
        media_dict.update(v_duration = track.duration)
        media_dict.update(v_bit_rate_mode = track.bit_rate_mode)
        media_dict.update(v_bit_rate = track.bit_rate)
        media_dict.update(v_max_bit_rate = track.maximum_bit_rate)
        media_dict.update(v_frame_rate = track.frame_rate)
        media_dict.update(v_frame_rate_mode = track.frame_rate_mode)
        media_dict.update(v_width = track.width)
        media_dict.update(v_height = track.height)
        media_dict.update(v_display_aspect_ratio = track.display_aspect_ratio)
        media_dict.update(v_standard = track.standard)
        media_dict.update(v_color_space = track.color_space)
        media_dict.update(v_chroma_sub = track.chroma_subsampling)
        media_dict.update(v_bit_depth = track.bit_depth)
        media_dict.update(v_scan_type = track.scan_type)
        media_dict.update(v_encoded_date = track.encoded_date)

    if track.track_type == 'Audio':
        media_dict.update(a_format = track.format)
        media_dict.update(a_format_info = track.format_info)
        media_dict.update(a_format_profile = track.format_profile)
        media_dict.update(a_codec_id = track.codec_id)
        media_dict.update(a_duration = track.duration)
        media_dict.update(a_bit_rate_mode = track.bit_rate_mode)
        media_dict.update(a_bit_rate = track.bit_rate)
        media_dict.update(a_max_bit_rate = track.maximum_bit_rate)
        media_dict.update(a_channel_positions = track.channel_positions)
        media_dict.update(a_sampling_rate = track.sampling_rate)
        media_dict.update(a_compression_mode = track.compression_mode)


# print(media_dict)

return media_dict
