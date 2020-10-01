#VIOCE BASED VOICE SEARCH
import speech_recognition as sr #pip install speechRecognition
import os
import wave
import contextlib
import subprocess
#install FFmpeg 

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import os
import time

import pyglet #pip install pyglet
import cv2 #pip install opencv-python

import subprocess as sp




r = sr.Recognizer()
l=3

video_path = []
sec = []

def takeInput():
    #It takes microphone input from the user and returns string output

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)

    videoToAudio(query)    
    #return query


def videoToAudio(word):
    #It converts video file to audio file using ffmpeg
    f_video = video_path[0]
    command = 'C:/FFmpeg/bin/ffmpeg -i '+f_video+' -ab 160k -ac 2 -ar 44100 -vn newaudio.wav'
    subprocess.call(command, shell=True)

    messagebox.showinfo(title='Processing...', message='Please wait, this may take some time...')

    wordSearch('newaudio.wav', word)


def audioToText(file):
    #It converts audio file to text format with all possible transcripts

    all_text=[]

    """ t is length of audio file """
    t=int(getTime(file))+5
    sec.append(t)
    """l is time gap between consecutive subtitle list """
    for i in range (0,t,l):
        r = sr.Recognizer()
        audio = sr.AudioFile(file)
        with audio as source:
    
            try:
                audio = r.record(source, duration=l,offset=i)
                text=(r.recognize_google(audio, show_all=True))
                all_text.append(text)
            
            except:
                all_text.append("NULL")
                continue
    
    return all_text


def getTime(file):
    #It calculates the duration of video(uses the audio form)
 
    fname = file
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def wordSearch(file, word):
    #this function searches the input in audio transcripts of the video and allows
    #the user to select timestamps to play the video

    transcripts = audioToText(file)
    tlength = (len(transcripts))
    time = []
    count = 0
    for i in transcripts:
        try:
            trans_list = (list(i.values())[0])
            count = count + 1
        except:
            continue
        for j in trans_list:
            if word in j['transcript']:
                time.append(count)
    output = []
    timestamp_list = []
    flag = 0
    for x in time:
        if x not in output:
            output.append(x)
    #print('timestamps :')
    for k in output:
        timestamp_list.append(k*l)
    if output==[]:
        flag = 1
    os.remove('newaudio.wav')
    
    window_3 = Tk()
    window_3.title('Voice Based Voice Search Output Selection')
    window_3.geometry('750x400')
    style = Style(window)
    style.theme_use("clam")

    lbl_Head = Label(window_3, text="Voice Bsed Voice Search", font=("Arial Bold", 22))
    lbl_Head.grid(column=1, row=0)

    lbl_ts = Label(window_3, text="Select timestamp :", font=("Arial Bold", 20))
    lbl_ts.grid(column=0, row=5)

    combo = Combobox(window_3)
    combo['values']= tuple(timestamp_list)
    combo.grid(column=2, row=5)

    #sec.append(int(combo.get()))
    #print(sec)

    t_button = Button(window_3, text="Play Video", command= lambda: playVideo(combo))
    t_button.grid(row=10, column=1, padx=4, pady=4)

    window_3.mainloop()



def playVideo(combo):
    #It plays the desired video from selected timestamp

    tm = int(combo.get())
    print(tm)
    durration = sec[0] - tm 

    v_file = video_path[0]

    def get_ffmpeg_bin():
        FFMPEG_BIN = os.path.join("C:/FFmpeg/bin", "ffmpeg.exe")
        return FFMPEG_BIN


    def split_vid_from_path(video_file_path, start_time, durration):
        ffmpeg_binary =  get_ffmpeg_bin()
        output_file_name = "test.mp4"
        pipe = sp.Popen([ffmpeg_binary,"-v", "quiet", "-y", "-i", video_file_path, "-vcodec", "copy", "-acodec", "copy",
                     "-ss", start_time, "-t", durration, "-sn", output_file_name ])


        pipe.wait()
        return True


    sample_vid =  v_file
    split_vid_from_path(sample_vid, "00:00:"+str(tm), "00:00:"+str(durration))

    os.popen("test.mp4")
    time.sleep(durration)
    os.remove("test.mp4")

def c_open_file_old():
    #It is used to take file input from user via browsing

    rep = filedialog.askopenfilenames(
        parent=window,
        initialdir='/',
        filetypes=[("All files", "*")])
    print(rep[0])
    fil = rep[0]
    video_path.append(fil)


window = Tk()
 
window.title("Voice Based Voice Search Input Window")
 
window.geometry('650x300')

style = Style(window)
style.theme_use("clam")

lbl_Heading = Label(window, text="Voice Based Voice Search", font=("Arial Bold", 22))
lbl_Heading.grid(column=1, row=0)

lbl_browse = Label(window, text="Select file :", font=("Arial Bold", 20))
lbl_browse.grid(column=0, row=5)

browse_button = Button(window, text="Open files", command=c_open_file_old)
browse_button.grid(row=5, column=20, padx=4, pady=4)

lbl_input = Label(window, text="Voice Input :", font=("Arial Bold", 20))
lbl_input.grid(column=0, row=10)

browse_button = Button(window, text="Take Voice Input", command=takeInput)
browse_button.grid(row=10, column=20, padx=4, pady=4)

# lbl_chapter = Label(window, text="Select timestamp :", font=("Arial Bold", 20))
# lbl_chapter.grid(column=0, row=15)

window.mainloop()

