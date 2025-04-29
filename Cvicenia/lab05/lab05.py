intervals = [
    ('Daniel', 7, 9),
    ('Palo', 8, 11),
    ('Danka', 10, 12),
    ('Miro', 9, 1),
    ('Lubos', 11, 12),
    ('Milan', 10, 12),
    ('Noro', 9, 11),
    ('Radka', 8, 10),
    ('Martina', 7, 8),
    ('Peto', 9, 11)
]

def load_intervals(intervals):
    # returns a list of intervals as tuples
    if not isinstance(intervals, list):
        raise TypeError(f"Expected type list, got{type(intervals)}")
    
    interval_list = []
    
    for line in intervals:
        if not isinstance(line, tuple):
            raise TypeError(f"Expected type tuple, got{type(line)}")
        if len(line) != 3:
            raise TypeError("Expected 3 parameters in each tuple")
        
        name, prichod, odchod = line
        if not isinstance(name, str) or not isinstance(prichod, int) or not isinstance(odchod, int):
            raise TypeError("Wrong type of value")
        if prichod == 6 or odchod == 6:
            raise ValueError("Wrong time! Party starts at 7pm and end at 5am")
        
        if odchod < 7:
            odchod += 12
        interval_list.append((prichod, odchod))
    
    return interval_list



def choose_time(intervals):
    # return best time to party and number of friends present
    interval_list = load_intervals(intervals)

    events = []
    for start, end in interval_list:
        events.append((start, 'start'))
        events.append((end, 'end'))
    events.sort

    max_count = 0
    best_time = 0
    pcount = 0
    for evt_time, evt_type in events:
        if evt_type == 'start':
            pcount += 1
        elif evt_type == 'end':
            pcount -= 1
        
        if pcount > max_count:
            max_count = pcount
            best_time = evt_time
    return best_time, max_count



