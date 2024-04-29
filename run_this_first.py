'''
READ THIS FIRST 

 How to use :

1° You need between 15 to 30 secondes of the voice you want to clone, it will be your reference voice.
   (You need a 44100Hz or 22050Hz mono 32bit float WAV file for best results. Audacity can help you with this.*)
2° Place your reference voice in "voices" folder.
3° Change "yield" and "language" according to your language. Don't use english text with language="fr" for exemple.
   Supported language : English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), 
   Dutch (nl),Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu) and Korean (ko)
4° Change the "voice" path according to the voice you want to clone. Exemple : "./voices/somethingsomething.wav"
5° Run the script. The first time, he will download the basic model and reference files to get xtts up and running.
6° When voice as play, stop the script and check your voices folder, you have now a new .json file with the same name as your reference voice.

Info :
 If the voice is not good or with bad accent, check "language" and "yield" or find a better audio sample.
 
 *If you don't know how to get clear reference voice, check some audiobook in your language on youtube, download them, use audacity to cut 45 secondes,
 remove long blank or long pause (more than 1 second) and save this segment into 44100Hz mono 32bit float WAV file.
 
 Everytime you want to add a different voice, redo 1° to 6°.
'''
from RealtimeTTS import TextToAudioStream, CoquiEngine

def dummy_generator():
    yield "Write something random for xtts to clone the voice and generate the file he need." # change this in your language, 1 or 2 phrases is ok.

if __name__ == '__main__':
    TextToAudioStream(CoquiEngine(voice="./voices/en_sample.wav", language="en"), log_characters=True).feed(dummy_generator()).play() 
    # ^ change "en_sample.wav" & "language" by yours.
