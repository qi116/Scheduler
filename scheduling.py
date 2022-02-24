from datetime import datetime
import random
import time
from icalendar import Calendar, Event
from pytz import UTC
import numpy as np
import pandas as pd

class OverlapFinderFast:
    def __init__(self,people:pd.DataFrame) -> None:
        self.people = people
        #print(self.people)
        self.people["S"] = 1
        self.people["E"] = -1
        #self.people.sort_values(by=["start","end"],inplace=True)
        starts = self.people.loc[:,["start","S"]].to_numpy()
        ends = self.people.loc[:,["end","E"]].to_numpy()
        self.people_flattened = np.concatenate((starts,ends),axis=0)
        #print(self.people_flattened)
        self.people_flattened = self.people_flattened[np.argsort(self.people_flattened[:, 0])]
        # print(self.people_flattened)
        # self.start_times = [(s[0],1) for s in self.people_flattened]
        # self.end_times = [(s[1],-1) for s in self.people_flattened]
        # #del self.people_flattened,self.people
        # self.all_times =self.start_times
        # self.all_times.extend(self.end_times)
        # self.all_times = sorted(self.all_times,key=lambda x:x[0])
    
    def parseCal(file):
        g = open(file,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('dtstart').dt , component.get('dtend').dt)
                #print(component.get('dtstamp'))
        g.close()
        
    def simulate_people(n):
        people = []
        for i in range(n):
            person = []
            for i in range(random.randint(1,5)):
                offset = random.randint(2,500) #change second number for wider time range
                person.append((random.random()*2+offset,random.random()*3+offset+3))
            people.append(person)
        all_events : list = []
        people_ids = []
        count = 1
        for person in people:
            all_events.extend(person)
            people_ids.extend([count]*len(person))
            count += 1
        #print(len(all_events),len(people_ids))
        df = pd.DataFrame({"start":[s[0] for s in all_events],"end":[s[1] for s in all_events],"person":people_ids})
        return OverlapFinderFast(df)
    
    def get_freetime(self):
        # print(self.people)
        tracker = np.cumsum(self.people_flattened[:,1])
        # print("tracker",tracker)
        freetime_starts = np.where(tracker==0)[0][:-1]
        # print("freetime",freetime_starts)
        freetime_ends = [] if len(freetime_starts) == 1 and freetime_starts[0] == len(tracker) -1 else freetime_starts + 1
        if len(freetime_ends) == 0:
            return np.array([])
        # print(self.people_flattened[freetime_starts,0])
        # print(self.people_flattened[freetime_ends,0])
        return np.column_stack((self.people_flattened[freetime_starts,0],self.people_flattened[freetime_ends,0]))
        

class OverlapFinder:
    def __init__(self,people) -> None:
        self.people = people
        #print(people)
        self.people_flattened = []
        for p in self.people:
            self.people_flattened.extend(p)
        self.people_flattened = sorted(self.people_flattened,key=lambda x:(x[0],x[1]))
        self.start_times = [(s[0],"S") for s in self.people_flattened]
        self.end_times = [(s[1],"E") for s in self.people_flattened]
        #del self.people_flattened,self.people
        self.all_times =self.start_times
        self.all_times.extend(self.end_times)
        self.all_times = sorted(self.all_times,key=lambda x:x[0])
    
    def parseCal(file):
        g = open(file,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('dtstart').dt , component.get('dtend').dt)
                #print(component.get('dtstamp'))
        g.close()
        
    def simulate_people(n):
        people = []
        for i in range(n):
            person = []
            for i in range(random.randint(1,5)):
                offset = random.randint(2,500) #change second number for wider time range
                person.append((random.random()*2+offset,random.random()*3+offset+3))
            people.append(person)
        return OverlapFinder(people)
    
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
    o = OverlapFinderFast.simulate_people(10**6)
    o2 = OverlapFinder.simulate_people(10**6)
    start = time.time()
    n = o.get_freetime()
    print("final fast:",n)
    print(time.time()-start," seconds")
    ###
    start = time.time()
    n2 = o2.get_freetime()
    print("final slow:",n2)
    print(time.time()-start," seconds")
    #OverlapFinder.parseCal("calendar.ics")