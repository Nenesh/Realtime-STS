# Realtime-Speech-to-Speech
Fast local Speech To Speech using [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) &amp; [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS)

I'm not the creator of RealTimeTTS or RealTimeSTT, I just make this script for fun and it work pretty well and fast for me with an i5 12600, 32Go of ram and an RTX 3060 12Go.

## How to install :
- conda create -n sts python=3.10
- conda activate sts

- pip install RealtimeSTT
- pip install RealtimeTTS

*You will get conflicting dependency errors, ignore it. (Can't do nothing about it, but it work fine)*

- **Be sure to have CUDA 11.8 install for your system (win10 link)=>** https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local

- pip install torch==2.1.2+cu118 torchaudio==2.1.2+cu118 --index-url https://download.pytorch.org/whl/cu118

*This will allow you to use GPU for xtts. You will get error about conflicting dependency for torch, ignore it.*
*(Can't do nothing about it, STT and TTS have different requirements on there requirements.txt but 2.1.2 work fine with the 2)*

- pip install keyboard

## How to use it :

Go in > run_this_first.py.

*It will download xtts model and generate the file you need to make every voice you want to work.*
*Read the comment on top of the script for instructions.*

- You can change personality of your bot by modifying personality.txt file.

In sts.py :
- All settings are between line 8 and 36. Comment will help you understand what they are for.
- Only thing you will maybe want to change is line 90 : Change "Emma" with your bot name.
- Launch LM Studio on server mode.

- Run sts.py script.

*Lauching take some time (30s to 40s), but ones is launch you can have a conversation close to realtime.*

- Wait for "speak now".
- If the response from the llm is to long for you, you can force stop the TTS by pressing spacebar.

### The script should work fine, but some you will see some problem in the console (warning message and double llm transcript), to fix that :

- Go to c:\Users\User\.conda\envs\sts\lib\site-packages\TTS\tts\layers\xtts\stream_generator.py
- Delet line 137 to 143 (the "if new_generation_config != self.generation_config:" statement)

Ones done, this part of the code should look like this :

            if self.generation_config._from_model_config:
                new_generation_config = StreamGenerationConfig.from_model_config(self.config)
                self.generation_config = new_generation_config
            generation_config = self.generation_config

- After that, in sts.py, right clic on CoquiEngine > Go to Definition
- or go to c:\Users\User\.conda\envs\sts\lib\site-packages\RealtimeTTS\engines\coqui_engine.py
- Comment line 547 like this:
> #print(f"XTTS Synthesizing: {text}")

## more info :
- spinner from "RealtimeSTT.AudioToTextRecorder" is set to False because sometime, he get stuck, I don't know why. I use some callback to do the same things.
- The script have no memory or rag yet.
