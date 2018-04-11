from generator import Generator


def run():
    gen = Generator('insta_geo.json', None)
    try:
        gen.process(800)
    except Exception as e:
        print('Error has occurred!')
        print("Error: ", str(e))
    finally:
        gen.__save__()

if __name__ == '__main__':
    run()


