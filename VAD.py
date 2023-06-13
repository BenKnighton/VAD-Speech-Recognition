import pyaudio
import webrtcvad
import wave
import time
from pydub import AudioSegment



VAD_p = pyaudio.PyAudio()
vad = webrtcvad.Vad(3)
VAD_frames = []
def Listener():
    VAD_rate = 16000
    chunkDuration = 30
    VAD_chunk = int(VAD_rate * chunkDuration / 1000)
    print(VAD_chunk)

    windowChunk = int(400 / chunkDuration)
    windowChunkEnd = windowChunk * 2

    VAD_stream = VAD_p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=VAD_rate,
                    input=True,
                    start=False,
                    frames_per_buffer=VAD_chunk)

    global VAD_frames
    triggered = False
    ring_buffer_flags = [0] * windowChunk
    ring_buffer_index = 0
    ring_buffer_flags_end = [0] * windowChunkEnd
    ring_buffer_index_end = 0
    StartTime = time.time()
    start_point_time = time.time()
    VAD_stream.start_stream()

    while True:
        data = VAD_stream.read(VAD_chunk, exception_on_overflow = False)
        VAD_frames.append(data)

        TimeUse = time.time() - StartTime
        active = vad.is_speech(data, VAD_rate)
        ring_buffer_flags[ring_buffer_index] = 1 if active else 0
        ring_buffer_index += 1
        ring_buffer_index %= windowChunk
        ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
        ring_buffer_index_end += 1
        ring_buffer_index_end %= windowChunkEnd
        if not triggered:
            global global_start_point_time
            global_start_point_time = time.time()
            num_voiced = sum(ring_buffer_flags)
            if num_voiced > 0.8 * windowChunk:
                triggered = True

        else:
            global end_point_time
            end_point_time = time.time()
            num_unvoiced = windowChunkEnd - sum(ring_buffer_flags_end)
            if num_unvoiced > 0.8 * windowChunkEnd or TimeUse > 15: #15
                triggered = False
                break

        # if time.time() - StartTime > 1:
        #     print("done")
        #     break
                
    VAD_stream.stop_stream()
    wf = wave.open("full.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(VAD_p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(VAD_rate)
    wf.writeframes(b''.join(VAD_frames))
    wf.close()
    startTime = (((end_point_time - start_point_time) - (end_point_time - global_start_point_time))-0.7)*1000
    endTime = +((end_point_time - start_point_time))*1000

    if (global_start_point_time)-0.75-start_point_time < 0.25:
        sound2 = AudioSegment.from_file("full.wav")
        sound1 = AudioSegment.from_file("ending.wav")
        combined_sounds = sound1 + sound2
        combined_sounds.export("ending.wav", format="wav") #2
    elif end_point_time - start_point_time < 2.5:
        myfile = AudioSegment.from_file("full.wav")
        myfile.export("ending.wav", format="wav")
    else:
        myfile = AudioSegment.from_file("full.wav")
        extract = myfile[startTime:endTime]
        extract.export("ending.wav", format="wav")
        
    VAD_frames.clear()
    VAD_stream.close()


Listener()

# import math
# import re

# def ellipsis_remover(number: str) -> float:
#     number = str(number)
#     counts = len(re.findall(r'(\w+)\.{3,}', number))
#     print(counts)
#     if counts == 0:
#         return number
#     elif counts == 1:
#         x = number.replace("...", "")
#         return str(round(float(x), 3))
#     elif counts > 1:
#         raise Exception("too many ellipsis!")


# text = ellipsis_remover(177245385090551602)
# print(text)
# text = ellipsis_remover(str("17724538509055160272981674833411451827975494561223871282138077898..."))
# print(text)



# from pydub import AudioSegment

# sil_duration = 0.3 * 1000
# one_sec_segment = AudioSegment.silent(duration = sil_duration)  #duration in milliseconds
# song = AudioSegment.from_wav("combined.wav")
# final_song =  song + one_sec_segment
# final_song.export("combined.wav", format="wav")

#Or Play modified audio
# play(final_song)