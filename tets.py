from pydub import AudioSegment
import numpy as np

# List of audio files and timings
audio_files = ['textaudios/16_0.mp3', 'FILLER', 'textaudios/16_1.mp3', 'FILLER', 'textaudios/16_2.mp3', 'FILLER', 'textaudios/16_3.mp3', 'FILLER']
timings = [1.752, 1.0, 6.384, 1.0, 9.96, 1.0, 8.208, 1.0]  # Adjusted timings in seconds
timings_array = np.array(timings) * 1000

# Load the stock music
stock_music = AudioSegment.from_file("stockmusic/default.mp3")

# Initialize the final audio segment
final_audio = AudioSegment.empty()

start_times = []
start_times.append(0)
i = 0
times_added_up = 0
while i < len(timings):
    print(times_added_up)
    times_added_up = times_added_up + timings_array[i]
    start_times.append(times_added_up)
    i += 1
    
# Load the stock music
stock_music = AudioSegment.from_file("stockmusic/default.mp3")
fade_duration = 1000
stock_music = stock_music.fade_in(fade_duration).fade_out(fade_duration)

# Initialize the final audio segment
final_audio = AudioSegment.empty()
    
start_times_array = np.array(start_times)
audio_files_array = np.array(audio_files)

x = 0
while x < len(audio_files):
    audiofile = audio_files_array[x]
    if audiofile != 'FILLER':
        audio = AudioSegment.from_file(audiofile)
        start_time = int(start_times_array[x]/1000)
        print('start time: ' + str(start_time))
        audio = audio[start_time:]
        final_audio += audio
    else:
        break_duration = timings_array[x]
        print('pause, duration: ' + str(break_duration))
        silent_segment = AudioSegment.silent(duration=break_duration)
        final_audio += silent_segment
    x += 1
    

# for audio_file, timing in zip(audio_files, start_times):
#     if audio_file != 'FILLER':
#         audio = AudioSegment.from_file(audio_file)
#         print(f"Loaded audio file: {audio_file}, Duration: {len(audio) / 1000} seconds")
# 
#         if timing != 10.0:
#             start_time = int(timing / 1000)  # Convert timing to milliseconds
#             audio = audio[start_time:]
# 
#         final_audio += audio
#     else:
#         break_duration = int(timing)  # Convert timing to milliseconds
#         silent_segment = AudioSegment.silent(duration=break_duration)
#         final_audio += silent_segment

# Mix the final audio and the stock music with reduced volume
final_audio_with_music = final_audio.overlay(stock_music - 20)

# Set the output file name and export the final audio
output_filename = "output_audio.mp3"
final_audio_with_music.export(output_filename, format="mp3")

# Calculate the total length of the final audio in seconds
total_length = len(final_audio_with_music) / 1000

print("Final audio saved as:", output_filename)
print("Total length:", total_length, "seconds")
