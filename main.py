from generator import Generator


def run():
    gen = Generator('insta_geo.json', None)
    gen.process(10)

if __name__ == '__main__':
    run()


