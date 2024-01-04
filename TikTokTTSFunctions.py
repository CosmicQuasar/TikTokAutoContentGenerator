from tiktokvoice import tts as tiktoktts
import pydub
import os

def sentence_parser(post: str) -> list: #takes in a long post and breaks it into sentences, appended to a list.
    sentence_list = []
    sentence = ''
    for value in post:
        if value in ['!', '?', '.']:
            sentence += value
            sentence_list.append(sentence.strip())
            sentence = ''
        else: 
            sentence += value
    if sentence:
        sentence_list.append(sentence.strip())
    return sentence_list

def gtts_loop(post_list: list[str]): #generates an mp3 file for each sentence, and puts it in a dict as {filepath: sentence, mp3 length}
    file_index = 0
    mp3_to_text_dict = {}
    for value in post_list: 
        file_name = 'Materials\\sentence' + str(file_index) + '.mp3' 
        mp3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        tiktoktts(value, 'en_us_001', mp3_file_path, False) #saves an mp3 file for each sentence in the form: sentence[number].mp3

        mp3_length = len(pydub.AudioSegment.from_mp3(mp3_file_path))/1000 #from milliseconds to seconds

        mp3_to_text_dict[mp3_file_path] = value, mp3_length
        file_index += 1
    return mp3_to_text_dict

def get_total_mp3_length(mp3_to_text_dict: dict): #returns total number of seconds to speak all mp3 files
    length = 0
    for key in mp3_to_text_dict:
        length += mp3_to_text_dict[key][1]
    return length

def delete_mp3_files(number_of_files: int): #deletes the created mp3 files. Use as: delete_mp3_files(len(**gtts_loop dict**))
    for i in range(number_of_files):
        file_name = 'Materials\\sentence' + str(i) + '.mp3' 
        mp3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        os.remove(mp3_file_path)


if __name__ == '__main__': #test
    txt_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Materials\\text.txt')
    text = open(txt_file_path, 'r')

    parsed_post = sentence_parser(text.read())
    mp3_to_text_dict = gtts_loop(parsed_post)
    print(get_total_mp3_length(mp3_to_text_dict))
    print(mp3_to_text_dict)

    #delete_mp3_files(len(mp3_to_text_dict))




