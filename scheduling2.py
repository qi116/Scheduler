from datetime import datetime
import random
import time
from icalendar import Calendar, Event
from pytz import UTC

class OverlapFinder:
    def __init__(self,*people) -> None:
        self.people = [i for i in people]
        self.people_flattened = []
        for p in self.people:
            self.people_flattened.extend(p)
        self.people_flattened = sorted(self.people_flattened,key=lambda x:(x[0],x[1]))
        self.start_times = [(s[0],"S") for s in self.people_flattened]
        self.end_times = [(s[1],"E") for s in self.people_flattened]
        del self.people_flattened,self.people
        self.all_times =self.start_times
        self.all_times.extend(self.end_times)
        self.all_times = sorted(self.all_times,key=lambda x:x[0])
    
    def parseCal(file):
        g = open(file,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('dtstart').dt  component.get('dtend').dt)
                #print(component.get('dtstamp'))
        g.close()
    
    def get_freetime(self):
        starts = 0
        ends = 0
        current_start = self.all_times[0]
        valid_intervals = []
        needed_time = .1 # this is arbitrary
        for i,s in enumerate(self.all_times):
            if i == 0:
                starts = 1
                continue
            if s[1] == "E":
                ends += 1
            else:
                starts+=1
            if ends == starts:
                if i == len(self.all_times) - 1:
                    continue
                else:
                    if self.all_times[i+1][0] - self.all_times[i][0] > needed_time:
                        valid_intervals.append((self.all_times[i][0],self.all_times[i+1][0]))
                starts = 0
                ends = 0
        return valid_intervals

if __name__ == "__main__":
    person1 = [(0,.5),(1,2),(2.1,2.4),(5,6),(6.2,7.2),(9,11.5),(12.5,3)]
    person2 = [(4,5.5),(9,12.7),(9,11.7),(12.5,3)]
    o = OverlapFinder(person1,person2)
    print(o.get_freetime())
    OverlapFinder.parseCal("calendar.ics")