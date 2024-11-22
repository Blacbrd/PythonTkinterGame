import os
import platform
import subprocess


def playMusic(musicPath):

    '''Plays music'''

    # Since different platforms should be able to play this game, I made the audio manager check what platform this comptuer is
    systemName = platform.system()

    if systemName == "Windows":

        # Need to import inside if statement otherwise error will be thrown on other systems
        import winsound

        winsound.PlaySound(musicPath, winsound.SND_ASYNC | winsound.SND_LOOP)
    
    elif systemName == "Linux":

        def linux_loop():

            while True:
                os.system(f"aplay -q {musicPath}")

        # Run the loop function as a background process
        subprocess.Popen(linux_loop)

    # MacOS
    elif systemName == "Darwin":

        def mac_loop():
            
            while True:
                os.system(f"afplay {musicPath}")

        # Run the loop function as a background process
        subprocess.Popen(mac_loop)
    
    else:

        print("Audio playback not supported with this OS")

# This allows me to stop all music, then play another track
def stopMusic():

    '''Stops music'''

    systemName = platform.system()

    if systemName == "Windows":

        import winsound

        # Stops any music that is currently being played
        winsound.PlaySound(None, winsound.SND_ASYNC)  

    elif systemName == "Linux":
        
        # Kill all aplay processes, stops the music
        os.system("killall aplay") 

    elif systemName == "Darwin":
        
        # Kill all afplay processes, stops the music
        os.system("killall afplay")  

    else:
        print("Audio playback not supported with this OS")