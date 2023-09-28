from listener.listener import Listener

def main():
    listener = Listener()
    try:
        listener.listen()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()