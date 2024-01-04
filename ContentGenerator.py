import TikTokTTSFunctions as TTT 
import VideoFunctions as VF 
import os

txt_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Materials\\text.txt')
text = open(txt_file_path, 'r')

parsed_post = TTT.sentence_parser(text.read())
mp3_to_text_dict = TTT.gtts_loop(parsed_post)
total_mp3_length = TTT.get_total_mp3_length(mp3_to_text_dict)

mp4_file_path = VF.video_path()
clip = VF.video_preprocessing(mp4_file_path, total_mp3_length)
clip = VF.attach_mp3s_to_video(clip, mp3_to_text_dict)
clip = VF.add_text(clip, mp3_to_text_dict)
VF.save_video(clip)

TTT.delete_mp3_files(len(mp3_to_text_dict))
