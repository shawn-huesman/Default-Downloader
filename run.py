# from defaultdownloader.app import create_app
from defaultdownloader.serv import linklist, youtube, misc

# app = create_app()

if __name__ == "__main__":
    linklist.run()
    youtube.run()
    misc.run()
    # app.run(host="0.0.0.0", port=5000)
