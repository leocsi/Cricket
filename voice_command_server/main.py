from speech_to_text.transcriber import Transcriber

def main():
    transcriber = Transcriber()
    try:
        transcriber.listen()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()