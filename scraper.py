#! /usr/bin/python
import urllib
import urllib2
from urllib import urlopen
import re
from xml.dom.minidom import parseString
import smtplib
import string
import os

def scrapepage():

    scBeginning = "http://api.soundcloud.com/tracks/"
    scStreamEnd = "/stream?client_id=9ef483d7c7eb439428d203f217ef8676"
    scDownloadEnd = "/download?client_id=9ef483d7c7eb439428d203f217ef8676"
    
    trackFile = open("tracks.txt", "r+")
    totalTracks = trackFile.read()
    
    emailList = []
    
    
    #-----------CHUBBYBEAVERS---------#
    
    emailList.append("Chubby Beavers\n---------------------------------------------------------")
    URL = "http://www.chubbybeavers.com"
    page = urlopen(URL).read()
    expression = re.compile('<p><a href="(.*)">')
    trackList = re.findall(expression, page)
    tempList = []
    
    for i in range(0, len(trackList)):
        if (string.find(trackList[i], ".mp3")!=-1):
            tempList.append(trackList[i])

    for k in range(0, len(tempList)):
        if (string.find(totalTracks, tempList[k])==-1):
            emailList.append(tempList[k])
            trackFile.write("%s\n" % tempList[k])


    #-----------MUSICNINJA------------#

    emailList.append("The Music Ninja\n--------------------------------------------------------")
    URL = "http://www.themusicninja.com"
    page = urlopen(URL).read()
    expression = re.compile('class="ninja_player long_layout" id="(.*)stream')
    trackList = re.findall(expression, page)
    for i in range(0, len(trackList)):
        id = trackList[i][33:41]
        if (string.find(totalTracks, id)==-1):
            emailList.append(scBeginning + id + scStreamEnd)
            emailList.append(scBeginning + id + scDownloadEnd)
            trackFile.write("%s\n" % id)

    #-----------EARMILK---------------#

    emailList.append("Earmilk\n----------------------------------------------------------------")
    URL = "http://www.earmilk.com"
    page = urlopen(URL).read()
    expression = re.compile('"url"(.*):')
    trackList = re.findall(expression, page)
    fileList = trackList[0].split(".mp3")
    for i in range(0, len(fileList)-1):
        k = len(fileList[i])-1
        track = "http:"
        while (fileList[i][k] != ':'):
            k-=1
        k+=1
        while (k<len(fileList[i])):
            if (fileList[i][k]!="\\"):
                track+=fileList[i][k]
            k+=1
        track+=".mp3"
        string.replace(track, "\\", "")
        if (string.find(totalTracks, track)==-1):
            emailList.append(track)
            trackFile.write("%s\n" % track)
        

    #-----------THEJACKPLUG-----------#

    URL = "http://www.thejackplug.com"
    emailList.append("The Jack Plug\n----------------------------------------------------------")
    page = urlopen(URL).read()
    expression = re.compile('2Ftracks(.*)&')
    trackList = re.findall(expression, page)
    for i in range(1, len(trackList)):
        id = trackList[i][3:11]
        if (string.find(totalTracks, id)==-1):
            emailList.append(scBeginning + id + scStreamEnd)
            emailList.append(scBeginning + id + scDownloadEnd)
            trackFile.write("%s\n" % id)
    

    #-----------DOTHEPANTSDANCE-------#

    URL = "http://www.dothepantsdance.com/blog"
    emailList.append("Do the Pants Dance\n-----------------------------------------------------")
    page = urlopen(URL).read()
    expression = re.compile('href="(.*)"')
    trackList = re.findall(expression, page)
    finalTrackList = []
    for i in range(0, len(trackList)):
        if (string.find(totalTracks, trackList[i])==-1):
            if (string.find(trackList[i], ".mp3")!=-1):
                wordlist = string.split(trackList[i])
                word = "http://www.dothepantsdance.com"+wordlist[0]
                string.rstrip(word, '"')
                if (word[len(word)-1]=='"'):
                    word = word[:len(word)-1]
                emailList.append(word)
                trackFile.write("%s\n" % trackList[i])


    #-----------ROBOTDANCEMUSIC-------#

    URL = "http://www.robotdancemusic.com/feed/"
    emailList.append("Robot Dance Music\n------------------------------------------------------")
    page = urlopen(URL).read()
    expression = re.compile('href="(.*)"')
    trackList = re.findall(expression, page)
    finalTrackList = []
    tempTotalTracks = ""
    for i in range(0, len(trackList)):
        if (string.find(trackList[i], ".mp3")!=-1):
            if (string.find(totalTracks, trackList[i])==-1):
                if (string.find(tempTotalTracks, trackList[i])==-1):
                    emailList.append(trackList[i])
                    trackFile.write("%s\n" % trackList[i])
                    tempTotalTracks+=trackList[i]
    

    #-----------PLAYLIST--------------#

    playlist = open("playlist.m3u", "w")
    for item in emailList:
        playlist.write("%s\n" % item)


    #-----------EMAIL-----------------#

    SUBJECT = "Music Ninja and Chubby Beavers Tracks"
    TO = **Enter email address here**
    FROM = **Enter email address here**

    i = 0
    text = ""
    while (i <len(emailList)):
        text += emailList[i] + "\n\n"
        i+=1

    BODY = string.join((
            "From: %s" % FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT ,
            "",
            text
            ), "\r\n")
    HOST = "smtp.**enter host here, i.e. gmail**.com"
    server = smtplib.SMTP(HOST,587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(**Enter username here**, **Enter password here**)
    server.sendmail(FROM, [TO], BODY)
    server.quit()

    return list


scrapepage()
