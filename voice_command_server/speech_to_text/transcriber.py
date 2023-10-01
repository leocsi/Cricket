from vosk import Model, KaldiRecognizer
import pyaudio
from speech_to_text.assistant.assistant_client import AssistantClient

class Transcriber:
    START_CUE = "cricket"
    END_CUE = "thanks"
    def __init__(self):
        self.model = Model(r"voice_command_server/en-model")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

        self.assistant_client = AssistantClient()

    def listen(self):
        command = ""
        capturing = False
        while True:
            data = self.stream.read(4096)

            if self.recognizer.AcceptWaveform(data):
                text = self.recognizer.Result()[1:-2].strip()[10:-1]
                print(text)
                start_position = text.find(Transcriber.START_CUE)
                end_position = text.find(Transcriber.END_CUE)
                if start_position != -1:
                    if end_position == -1:
                        command += text[start_position+len(Transcriber.START_CUE):].strip() 
                        capturing = True
                    else:
                        command += text[start_position+len(Transcriber.START_CUE):end_position].strip()
                        print("Command: "+command)
                        command = ""
                
                elif capturing:
                    if end_position != -1:
                        command += ' ' + text[:end_position].strip()
                        capturing = False
                        print("Command: "+command)
                        command = ""
                    else:
                        command += ' ' + text.strip()
            command = command.strip()