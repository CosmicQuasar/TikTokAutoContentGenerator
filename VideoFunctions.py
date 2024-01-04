from moviepy.editor import *
import os

def video_path(video_name= 'backgroundvideo.mp4'): #gets the path of the mp4 file
    video_name = 'Materials\\' + video_name
    mp4_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), video_name)
    return mp4_file_path

def video_preprocessing(mp4_path: str, video_required_length: float): #cuts audio to appropriate length and removes audio
    clip = VideoFileClip(mp4_path)
    clip = clip.subclip(0, video_required_length)
    clip = clip.without_audio()
    return clip

def save_video(clip: VideoFileClip):
    clip.write_videofile(video_path(video_name= 'ContentVideo.mp4'))

def attach_mp3s_to_video(clip: VideoFileClip, mp3_file_dict: dict): #stitches together all the mp3 files and adds this mp3 file onto the video clip
    mp3_file_paths = list(mp3_file_dict.keys())
    mp3_initialized_list = []
    for file_path in mp3_file_paths:
        mp3_initialized = AudioFileClip(file_path)
        mp3_initialized_list.append(mp3_initialized)
    full_mp3 = concatenate_audioclips(mp3_initialized_list)
    clip = clip.set_audio(full_mp3)
    return clip
    
def add_text(clip: VideoFileClip, mp3_file_dict: dict):
    mp3_sentence_list = []
    mp3_length_list = []
    for key in mp3_file_dict:
        mp3_sentence_list.append(mp3_file_dict[key][0])
        mp3_length_list.append(mp3_file_dict[key][1])
    
    mp4_finished_clip_list = []
    for i in range(len(mp3_sentence_list)):
        if i == 0:
            start = 0
        else:
            start = sum(mp3_length_list[:i])
        end = start + mp3_length_list[i]
        clip_part = clip.subclip(start, end)
        text = TextClip(mp3_sentence_list[i], font= 'impact', fontsize= 50, color= 'white', stroke_color= 'black', stroke_width= 2, method= 'caption', size= [1000, 1000])
        text = text.set_position('center').set_duration(end - start)
        mp4_finished_clip = CompositeVideoClip([clip_part, text])
        mp4_finished_clip_list.append(mp4_finished_clip)

    full_mp4 = concatenate_videoclips(mp4_finished_clip_list)
    return full_mp4


if __name__ == '__main__':
    file_path = video_path()
    clip = video_preprocessing(file_path, 65.16)

    myDict = {'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence0.mp3': ('I (27f) have been married my husband(28M) for 2 years and gave birth to our daughter 5 weeks ago.', 7.32), 'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence1.mp3': ("I'll try to keep this short so I don't waste your time with any irrelevant details.", 5.208), 'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence2.mp3': ('What happened was that our daughter came out with blonde hair and pale blue eyes, while my husband and I have brown hair and brown eyes.', 8.232), 'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence3.mp3': ('My husband freaked out at this and refused to listen to my explanation that, sometimes, babies are born with lighter hair and eyes that get darker over time.', 10.248), 'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence4.mp3': ("He demanded a paternity test and threatened to divorce me if I didn't comply, so I did\n\nAfter my daughter and I got home from the hospital, my husband went to stay at his parents' house for the first three weeks to get some space from me, while I recovered and he told them what was happening.", 17.856), 'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence5.mp3': ('My MIL called and informed me that if the paternity test revealed that the child wasn\'t his, she would do anything within her power to make sure that I was " taken to the cleaners" during the divorce.', 11.856), 'c:\\Users\\super\\Desktop\\ContentGenerator\\sentence6.mp3': ('I had my sister to lean on and help me take care of the baby during this.', 4.44)}
    newclip = attach_mp3s_to_video(clip, myDict)
    newclip = add_text(newclip, myDict)
    save_video(newclip)