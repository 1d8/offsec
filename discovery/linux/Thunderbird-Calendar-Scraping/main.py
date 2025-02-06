import sqlite3
import os
import re

def fileExists():
    baseDir = os.path.expanduser("~/.thunderbird")
    for dirName in os.listdir(baseDir):
        if "release" in dirName:
            filePath = baseDir + f"/{dirName}/calendar-data/local.sqlite"
            if os.path.isfile(filePath):
                print(f"[+] Thunderbird SQLITE datbase found: {filePath}")
                return filePath

def parseDB(filePath):
    if filePath != None:
        print(f"[+] Parsing {filePath}...")
        conn = sqlite3.connect(filePath)
        c = conn.cursor()
        c.execute("SELECT cal_id, id, title, event_start, event_end  FROM cal_events")
        events = c.fetchall()
        
        for info in events:
            calendarID = info[0]
            eventID = info[1]
            eventTitle = info[2]
            eventStart = info[3]
            eventEnd = info[4]
            
            c.execute("SELECT icalSTring FROM cal_attendees WHERE item_id = ? AND cal_id = ?", (eventID, calendarID))
            attendees = c.fetchall()
            
            c.execute("SELECT key, value FROM cal_properties WHERE item_id = ? AND cal_id = ?", (eventID, calendarID))
            location = c.fetchall()

            c.execute("SELECT icalString FROM cal_attachments WHERE item_id = ? AND cal_id = ?", (eventID, calendarID))
            attachments = c.fetchall()
            
            
            rPattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

            if len(attendees) > 0:
                print(f"Event title: {eventTitle}\nEvent location: {location}\nEvent attachments:{attachments}")
                for i in attendees:
                    #print(f"Event attendees: {i[0].split(';')}")
                    emailAddr = re.findall(rPattern, i[0])
                    #print(emailAddr)
                    print(f"{i[0].split(';')[0]}: {emailAddr}")
            else:
                print(f"Event title: {eventTitle}\nEvent location: {location}\nEvent attachments: {attachments}")

        conn.close()



if __name__ == '__main__':
    path = fileExists()
    parseDB(path)


