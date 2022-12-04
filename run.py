from flask import Flask
from flask import render_template

from defaultdownloader.Database import DefaultDB
from defaultdownloader import serv

from defaultdownloader.app import create_app

app = create_app()

"""
def main():
    serv_linklist.run()
    serv_youtube.run()


if __name__ == "__main__":
    main()
"""

if __name__ == "__main__":
    # print(DefaultDB.youtube_get_videos())
    serv.linklist.run()
    serv.youtube.run()
    app.run(host="0.0.0.0", port=5000)
