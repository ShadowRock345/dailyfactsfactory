from mutagen.mp3 import MP3
import glob


def get_mp3_length(file_path):
    audio = MP3(file_path)
    return audio.info.length

def all_matching_tts_files(tts_path,id):
    pattern = tts_path + '/' + str(id) + '*'
    files = glob.glob(pattern)
    return files


music = []
music_files_sorted = []
filename = 54
id = 3
stockmusic_file_path = 'stockmusic/' + str(filename) + '.mp3'
tts_path = 'textaudios'

matching_files = all_matching_tts_files(tts_path,id)

intro = str(tts_path) + '/' + str(id) + '_0.mp3'
introlength = get_mp3_length(intro)
music.append(introlength)
music.append('0.3')
music_files_sorted.append(intro)
music_files_sorted.append('FILLER')

if intro in matching_files:
    matching_files.remove(intro)
    print('removed intro file')

for file in matching_files:
    factlength = get_mp3_length(file)
    music.append(factlength)
    music.append('0.3')
    music_files_sorted.append(file)
    music_files_sorted.append('FILLER')

final_video_lenght = 0
for element in music:
    final_video_lenght = final_video_lenght + float(element)

print(music)
print(music_files_sorted)
print(final_video_lenght)

