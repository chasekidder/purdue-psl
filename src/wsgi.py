import sys
import os
#sys.path.append(os.getcwd() + os.sep)

from src.modules.webui.frontend import app

if __name__ == "__main__":
    app.run()
