import re
from datetime import datetime, timedelta

week_days = { "MON" : {
    "A1": "08:00",
    "L1": "08:00",
    "L2": "08:50",
    "F1": "09:00",
    "D1": "10:00",
    "L3": "09:50",
    "L4": "10:40",
    "TB1": "11:00",
    "TG1": "12:00",
    "L5": "11:40",
    "L6": "12:30",
    "A2": "14:00",
    "L31": "14:00",
    "L32": "14:50",
    "F2": "15:00",
    "D2": "16:00",
    "L33": "15:50",
    "L34": "16:40",
    "TB2": "17:00",
    "TG2": "18:00",
    "L35": "17:40",
    "L36": "18:30",
    "V3": "19:00",
},

"TUE" : {
    "B1": "08:00",
    "L7": "08:00",
    "L8": "08:50",
    "G1": "09:00",
    "E1": "10:00",
    "L9": "09:50",
    "L10": "10:40",
    "TC1": "11:00",
    "TAA1": "12:00",
    "L11": "11:40",
    "L12": "12:30",
    "B2": "14:00",
    "L37": "14:00",
    "L38": "14:50",
    "G2": "15:00",
    "E2": "16:00",
    "L39": "15:50",
    "L40": "16:40",
    "TC2": "17:00",
    "TAA2": "18:00",
    "L41": "17:40",
    "L42": "18:30",
    "V4": "19:00",
},

"WED" : {
    "C1": "08:00",
    "L13": "08:00",
    "L14": "08:50",
    "A1": "09:00",
    "F1": "10:00",
    "L15": "09:50",
    "L16": "10:40",
    "V1": "11:00",
    "V2": "12:00",
    "L17": "11:40",
    "L18": "12:30",
    "C2": "14:00",
    "L43": "14:00",
    "L44": "15:00",
    "A2": "15:00",
    "F2": "16:00",
    "L45": "15:50",
    "L46": "16:40",
    "TD2": "17:00",
    "TBB2": "18:00",
    "L47": "17:40",
    "L48": "18:30",
    "V5": "19:00",
},

"THU" : {
    "D1": "08:00",
    "L19": "08:00",
    "L20": "08:50",
    "B1": "09:00",
    "G1": "10:00",
    "L21": "09:50",
    "L22": "10:40",
    "TE1": "11:00",
    "TCC1": "12:00",
    "L23": "11:40",
    "L24": "12:30",
    "D2": "14:00",
    "L49": "14:00",
    "L50": "14:50",
    "B2": "15:00",
    "G2": "16:00",
    "L51": "15:50",
    "L52": "16:40",
    "TE2": "17:00",
    "TCC2": "18:00",
    "L53": "17:40",
    "L54": "18:30",
    "V6": "19:00",
},

"FRI" : {
    "E1": "08:00",
    "L25": "08:00",
    "C1": "09:00",
    "TA1": "10:00",
    "L27": "09:50",
    "L28": "10:40",
    "TF1": "11:00",
    "TD1": "12:00",
    "L29": "11:40",
    "L30": "12:30",
    "E2": "14:00",
    "L55": "14:00",
    "L56": "14:50",
    "C2": "15:00",
    "TA2": "16:00",
    "L57": "15:50",
    "L58": "16:40",
    "TF2": "17:00",
    "TDD2": "18:00",
    "L59": "17:40",
    "L60": "18:30",
    "V7": "19:00",
}
}

n = 50 #define slot time interval

already = {
    "MON": {},
    "TUE": {},
    "WED": {},
    "THU": {},
    "FRI": {}
}

time_format_str = "%H:%M" # define format

def format_time(slot_time):
    """Function to convert time to Date time from string"""
    if len(slot_time) >= 5:
        return datetime.time(hour=int(slot_time[0:2]), minute=int(slot_time[3:5]))

def fetch_time(slot):
    """Function that returns timing of class"""
    for days in week_days.keys():
        for slots, timings in week_days[days].items():
            if slot == slots:
                if slots not in already[days]:
                    already[days][slots] = timings
                    return timings, days
    return None


def fetch_info(text):
    """Get slot data"""
    data, slots = [], []
    slots += re.findall(
        r"[A-Z]{1,3}[0-9]{1,2}[\D]{1}[A-Z]{3}[0-9]{4}[\D]{1}[A-Z]{2,3}[\D]{1}[A-Z]{2,4}[0-9]{2,4}[A-Z]{0,1}[\D]{1}[A-Z]{3}",
        text,
    )
    for single_slot in slots:
        slot = re.findall(r"[A-Z]{1,3}[0-9]{1,2}\b", single_slot)[0]
        course_name = re.findall(r"[A-Z]{3}[0-9]{4}\b", single_slot)[0]
        course_code = re.findall(r"[ETH,SS,ELA,LO]{2,3}\b", single_slot)
        course_type = "Lab" if course_code[0] in ("ELA", "LO") else "Theory"
        venue = re.findall(r"[A-Z]{2,4}[0-9]{2,4}[A-Z]{0,1}\b", single_slot)[1]
        resp = fetch_time(slot)
        startTime = resp[0]
        slot_day = resp[1]
        add_mins = datetime.strptime(startTime, time_format_str)
        endTime = add_mins + timedelta(minutes=n)

        endTime = endTime.strftime('%H:%M')

        slot_data = {
            "Slot": slot,
            "Course_Name": course_name,
            "Course_type": course_type,
            "Venue": venue,
            "Day": slot_day,
            "StartTime": startTime,
            "EndTime": endTime,
        }
        data.append(slot_data)
    return {"Slots": data}
