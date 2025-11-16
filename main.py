import os
import shutil

from app_UI import AppUI


if __name__ == "__main__":

    # create .env file if it doesn't exists
    if not os.path.exists('.env'):
        shutil.copyfile('.env_model', '.env')

    AppUI().launch_ui()

    