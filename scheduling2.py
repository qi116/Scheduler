from datetime import datetime
import random
import time
from icalendar import Calendar, Event
from pytz import UTC
import numpy as np
import pandas as pd


"""
A numpy and pandas approach to formatting timeslot data and finding unoccupied time slots
"""
class OverlapFinderFast:
    def __init__(self,people:pd.DataFrame) -> None:
        self.people = people
        self.people["S"] = 1
        self.people["E"] = -1
        #these variables are intermediates that are not stored
        starts = self.people.loc[:,["start","S"]].to_numpy() #directly from pandas to numpy Nx2 array for start_times
        ends = self.people.loc[:,["end","E"]].to_numpy() #directly from pandas to numpy Nx2 array for end_times
        # stack Nx2 arrays creating 2Nx2 array of all starts and ends, marked by (value,1) and (value,-1)
        self.people_flattened = np.concatenate((starts,ends),axis=0)
        #sort by the values while keeping the -1,1 labels
        self.people_flattened = self.people_flattened[np.argsort(self.people_flattened[:, 0])]
    
    def parseCal(file):
        g = open(file,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('dtstart').dt , component.get('dtend').dt)
                #print(component.get('dtstamp'))
        g.close()

    """
    Create n number of people, each containing a random # of events at random times, formatted as a Dense Dataframe
    TODO read this dataframe from sql records directly
    """
    def simulate_people(n):
        people = []
        for i in range(n):
            person = []
            for i in range(random.randint(5,5)):
                offset = random.randint(2,10**6) #change second number for wider time range
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
    
    """
    This is like the balancing bracket expresions algorithm, except we assume the expression is already matched, allowing us to easily find unoccupied periods of time whenever the cumulative start_times+end_times = 0. 
    """
    def get_freetime(self):
        #accumulating the -1 and 1 values means whenever the cumcum = 0, free time begins, and free time ends at the time of the next "1" event
        tracker = np.cumsum(self.people_flattened[:,1])
        #get indices of 0's in cumsum
        freetime_starts = np.where(tracker==0)[0][:-1]
        #freetime periods are guaranteed to end at the freetime_start_index + 1
        if len(freetime_starts) == 1 and freetime_starts[0] == len(tracker) -1:
            #this occurs if there is no free time discovered
            return np.array([])
        freetime_ends = freetime_starts + 1
            
        #reformat flattened start and end times into [[start_time,end_time],[start_time,end_time],...]
        return np.column_stack((self.people_flattened[freetime_starts,0],self.people_flattened[freetime_ends,0]))
        
"""
A pure python approach to formatting timeslot data and finding unoccupied time slots
"""
class OverlapFinder:
    def __init__(self,people) -> None:
        self.people = people
        #print(people)
        self.people_flattened = [] #1-d list to store time slots
        for p in self.people:
            self.people_flattened.extend(p)
        self.people_flattened = sorted(self.people_flattened,key=lambda x:(x[0],x[1])) #sort by start time then end time
        self.start_times = [(s[0],"S") for s in self.people_flattened] #convert start and end times to labelled tuples
        self.end_times = [(s[1],"E") for s in self.people_flattened]
        #del self.people_flattened,self.people
        self.all_times =self.start_times
        self.all_times.extend(self.end_times) #merge start and end tuples into a continuous list
        self.all_times = sorted(self.all_times,key=lambda x:x[0]) #sort all start and end times by their time value
    
    def parseCal(file):
        g = open(file,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('dtstart').dt , component.get('dtend').dt)
                #print(component.get('dtstamp'))
        g.close()
    
    """
    Create n number of people, each containing a random # of events at random times, formatted as 3D list
    """
    def simulate_people(n):
        people = []
        for i in range(n):
            person = []
            for i in range(random.randint(5,5)):
                offset = random.randint(2,10**6) #change second number for wider time range
                person.append((random.random()*2+offset,random.random()*3+offset+3))
            people.append(person)
        return OverlapFinder(people)
    
    """
    This is like the balancing bracket expresions algorithm, except we assume the expression is already matched, allowing us to easily find unoccupied periods of time whenever the cumulative start_times+end_times = 0
    """
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

def main():
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
if __name__ == "__main__":
    main()