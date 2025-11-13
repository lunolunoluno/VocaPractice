import os
import shutil

from sentence_generator import SentenceGenerator

if __name__ == "__main__":

    # create .env file if it doesn't exists
    if not os.path.exists('.env'):
        shutil.copyfile('.env_model', '.env')

    sg = SentenceGenerator()

    print(sg.generate_sentences())


    