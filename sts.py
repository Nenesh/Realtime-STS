import logging
import RealtimeSTT
import RealtimeTTS
from openai import OpenAI
import keyboard
import time
  

# path of your reference voice. The one you used in run_this_first.py . Default is set to xtts english sample.
tts_ref_voice = "./voices/en_sample.wav"

# Supported languages : English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), 
# Dutch (nl),Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu) and Korean (ko)
tts_language = "en"

# xtts "reading/talking" speed, 1.1 or 1.2 is good.
tts_speed = 1.2

# Temperature for the xtts model.
tts_temp = 0.85

# If xtts cut too much during speech, increase "buffer_threshold_seconds" to 2 or 3. 
# Higher number = more continuity of audio playback. 
# 0 to deactivate.
tts_buffer = 2

# Faster_whisper model. For english, use "tiny.en", "small.en", "medium.en" model. 
# For other languages than english, use "tiny", "small", "medium".
fw_model = "medium"

# Time in seconds of silence that must follow speech before the recording is considered to be completed. 
# This ensures that any brief pauses during speech don't prematurely end the recording.
post_speech_silence = 1 

# Temperature of LM Studio llm.
llm_temp = 0.85



# open_file to read personality.txt
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def voice_detect_start():
    print("Speak ...")
def voice_detect_stop():
    print("Voice detected")
def record_start():
    print("Recording ...")
def record_stop():
    print("Recording Stop")
def transcrib_start():
    print("\nTranscribing ...")



if __name__ == '__main__':
    
    # LM Studio endpoint
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    
    # use local .txt has caracter_prompt
    character_prompt = open_file("personality.txt")
    
    # Xtts settings. Mouseover CoquiEngine to see other variables.
    stream = RealtimeTTS.TextToAudioStream(RealtimeTTS.CoquiEngine(speed=tts_speed, temperature=tts_temp, voice=tts_ref_voice, language=tts_language), log_characters=True)
    
    # faster_whisper settings. Mouseover AudioToTextRecorder to see other variables.
    recorder = RealtimeSTT.AudioToTextRecorder(
        model=fw_model, spinner=False, post_speech_silence_duration=post_speech_silence, debug_mode=False, level=logging.ERROR, 
        on_vad_detect_start=voice_detect_start, 
        on_vad_detect_stop=voice_detect_stop, 
        on_recording_start=record_start, 
        on_recording_stop=record_stop, 
        on_transcription_start=transcrib_start)

    # LLM responce generator.
    def generate(messages):
        for chunk in client.chat.completions.create(model="local-llm", messages=messages, temperature=0.85, stream=True):
            text_chunk = chunk.choices[0].delta.content if chunk.choices else None
            if text_chunk:
                yield text_chunk   
    
      
    history = []
    while True:

        # change "Emma" with your chatbot name.
        print(f'User: {(user_text := recorder.text())}\nEmma: ', end="", flush=True)
        history.append({'role': 'user', 'content': user_text})
        assistant_response = generate([{'role': 'system', 'content': character_prompt}] + history[-10:])
        stream.feed(assistant_response)
        stream.play_async(buffer_threshold_seconds = tts_buffer, language = tts_language)
        #press spacebar to stop xtts, usefull if generated text is too long or bug and you want to stop it.

        while stream.is_playing():
            if keyboard.is_pressed('space'):
                stream.stop()
                print("FORCED STOP")
                break
            time.sleep(0.1)
            
        history.append({'role': 'assistant', 'content': stream.text()})