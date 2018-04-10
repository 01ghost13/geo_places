from generator import Generator


def run():
    try:
        gen = Generator('insta_geo.json', None)
        gen.process(5)
    except Exception:
        print('Error has occurred!')

if __name__ == '__main__':
    run()


