from gtts import gTTS
import os
from mpyg321.MPyg123Player import MPyg123Player
import time

class MyPlayer(MPyg123Player):
    """We create a class extending the basic player to implement callbacks"""

    onMusicEnd = None

    def __init__(self, onMusicEnd = None) -> None:
         self.onMusicEnd = onMusicEnd

    def on_any_stop(self):
        """Callback when the music stops for any reason"""
        print("The music has stopped")

    def on_user_pause(self):
        """Callback when user pauses the music"""
        print("The music has paused")

    def on_user_resume(self):
        """Callback when user resumes the music"""
        print("The music has resumed")

    def on_user_stop(self):
        """Callback when user stops music"""
        print("The music has stopped (by user)")

    def on_music_end(self):
        """Callback when music ends"""
        print("The music has ended")
        if self.onMusicEnd != None:
            self.onMusicEnd()

    def on_user_mute(self):
        """Callback when music is muted"""
        print("The music has been muted (continues playing)")

    def on_user_unmute(self):
        """Callback when music is unmuted"""
        print("Music has been unmuted")

def getMillis():
    return time.time_ns() // 1_000_000

def createMp3(text):
    tts = gTTS(text, lang='en', tld='com.au')
    filename = f'tts_{getMillis()}.mp3'
    tts.save(filename)
    print(f'Saved {filename}')
    return filename

def play(filename):
    player = MyPlayer()
    player.play_song(filename)

def removeTempFile(filename):
    os.remove(filename)

def playNowWithWrite(text):
    filename = createMp3(text)
    def clean():
        removeTempFile(filename)
        print('deleted file', filename)
    player = MyPlayer(clean)
    player.play_song(filename)