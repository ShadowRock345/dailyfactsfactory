from moviepy.editor import *

# Pfade zu den Dateien festlegen
stock_video_path = "video.mp4"
stock_music_path = "music.mp3"
font_path = "Pfad_zu_einer_Schriftart.ttf"

# Video- und Audio-Clips erstellen
video_clip = VideoFileClip(stock_video_path)
audio_clip = AudioFileClip(stock_music_path)

# Groesse und Position der Box für den Titel festlegen
box_width = video_clip.w // 2
box_height = video_clip.h // 6
box_x = video_clip.w // 4
box_y = video_clip.h // 2 - box_height // 2

# Hintergrund für die Box erstellen
#box_bg = ColorClip((box_width, box_height), color=(0, 0, 0), duration=5)

# Text für den Titel und den Fakt festlegen
title_text = "Boys Fakt"
fact_text = "Wusstes du, dass Boys Fakten langweilig sind?"
name_text = "@name"

# Text-Clips für den Titel, den Fakt und den Namen erstellen
title_clip = TextClip(title_text, fontsize=40, color="white").set_position((box_x + 10, box_y + 10)).set_duration(5)
fact_clip = TextClip(fact_text, fontsize=30, color="white").set_position((box_x + 10, box_y + 60)).set_duration(5)
name_clip = TextClip(name_text, fontsize=20, color="white").set_position((10, video_clip.h - 30)).set_duration(5)

# Clips zusammenfügen
final_clip = CompositeVideoClip([video_clip, title_clip, fact_clip, name_clip])
final_clip = final_clip.set_audio(audio_clip)

# Video exportieren
final_clip.write_videofile("Ausgabedatei.mp4", codec="libx264", fps=24)


