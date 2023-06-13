# VAD
The speech recognition was one of the most difficult aspects of my A.I, however the final result is spectacular. My version of speech recognition use voice activated detection (VAD). This allows me to do many things typical speech recognition frameworks, like Appel’s can’t do. It works a lot more similar to how humans process information.

## How it works
An audio stream is designated to the VAD, which once it recognises someone is speaking, makes a note of the time. When the person is done talking, the VAD finishes, and the stream closes. A small amount of time is retracted from the point where the VAD started, just to ensure the full sentence is processed, and then this time is used to trim the larger audio file that was recorded in the first channel. The resulting audio file is saved, and this is the file that the speech recognition neural network uses to retrieve a result.

## Cases
I had to take may things into account, like Lound noises, (by automatically adjusting the VAD threshold)
If I start talking, and it finishes and responds too quickly I can keep talking over it. It will pick up and add the previous audio file. This creates one big audio file, which has both halves of the conversation in it. This effectively means I can do speech recognition on my entire split sentence.

## Method
I used 5 different arrays contain different types of audio frames, 4 different Boolean True/False statements, and 5 different timing variables, and too many functions to count.
Eventually, though a complicated web of appending and clearing audio frames, adjusting audio files, and renormalising audio using all manner of filters, I eventually come up with one of the most realistic speech recognition algorithms, that all comes together and works to absolute perfection.

## How to use
Simply run the script, it will start recording. When it detects a voice, it strips the audio file from when it first detects talking (minus a small amount of time to ensure the voice is fully captured) to when the talking has finished, then speech recognition can be done on the file, using any kind of speech recognition library.

