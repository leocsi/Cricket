from listener.listener import Listener

def main():
    listener = Listener()
    try:
        listener.listen()
    except Exception as e:
        print(e.message())

if __name__ == '__main__':
    main()