import datetime
import os
import random
import pandas as pd

def load_line_infos(path):  # 2 points
    # loads timetables from the specified path and returns them in a dictionary
    # dictionary structure:
    #  - keys are line numbers (as integers)
    #  - each value is a list of tuples describing information on a stop
    #  - for the first stop, the tuple contains the name of the city
    #    and a list of all start times
    #  - start times are tuples with hour and minutes as integers
    #  - for all other stops, the tuple contains the city name
    #    and the number of minutes it takes to get there from the previous stop
    my_dict = {}
    with open(path, "r", encoding="utf-8") as my_file:
        for line in my_file:
            key, value = line.rstrip().split(";",1)     #spracovanie na key a hodnotu
            key = int(key)
            value = value.split(";")        #rozdeli do stringov podla miest
            new = []        #novy zoznam pre hodnuty klucov

            for x in value:
                city, times = x.split(",",1)    #rozdeli na mesto a casy
                                
                if len(times) > 2:      
                    times = times.split(",")
                    processed_times = []        #zoznam pre upravene casy v tuploch
                    for time in times:
                        hour, minute = time.split(":")
                        processed_times.append((int(hour), int(minute)))        #pridavanie tuploch do zoznamu
                    times = processed_times         #tu sa zoznam s casmi nahradi zoznamom kde su casy v tuploch
                else:
                    times = int(times)
                
                new.append((str(city), times))      #ulozenie miest a spracovanych casoch do zoznamu
            
            my_dict[key] = new

    return my_dict



def find_next_train(line_infos, line, hour, minute=0):  # 1
    # the function generates the scheduled timetable for the next train
    # on a given line
    # inputs:
    #  - line_infos: dictionary with line information (as loaded by load_line_infos)
    #  - line: the number of the line we are interested in (integer)
    #  - hour: the hour when we start our search (integer)
    #  - minute: the minute when we start our search (integer, by default 0)
    # the function returns a list of tuples where each tuple has two values:
    #  - city name (string)
    #  - a tuple representing the time when the train is scheduled to arrive
    #  - the train stands for a minute at each stop (if it arrives at 10:15,
    #    it leaves at 10:16, if the next stop is 5 minute away, it will arrive
    #    there at 10:21, not 10:20)
    if line not in line_infos:
        return None

    values = line_infos[line]       #cely zoznam s casmi a zastavkami
    start_times = values[0][1]      #casy kedy vuraza 
    start_city = values[0][0]       #mesto zkade zacina

    next_train = None
    for time in start_times:
        if (time[0] > hour) or (time[0] == hour and time[1] >= minute):
            next_train = time     #najblizsi spoj  
            break
    
    if next_train is None:
        next_train = start_times[0]
    
    train = [(start_city, next_train)]      #startovaci cas
    current_time = list(next_train)
    
    next_stop  = 1
    next_time = (time[0], time[1])      #zakladny cas
    while next_stop < len(values):      #prechadza cez zvysne zastavky okrem prvej
        next_city = values[next_stop][0]        #nove mesto
        travel_minutes =  values[next_stop][1]
        total_minutes = travel_minutes

        if next_stop > 1:
            total_minutes +=1

        current_minutes = current_time[1] + total_minutes
        current_hours = current_time[0] + (current_minutes // 60)
        current_minutes = current_minutes % 60

        current_time = [current_hours, current_minutes]
        train.append((next_city, tuple(current_time)))        #pridanie do vysledneho zoznamu, doplnanie za startovny cas
        next_stop += 1

    return train
    


def get_city_timetable(line_infos, city):  # 2
    # the function generates the timetable for an arbitrary city
    # for each line with regards to the end station
    # inputs:
    #  - line_infos: dictionary with timetable (as loaded by load_line_infos)
    #  - city: the city for which we want to generate the timetable (string)
    # the function returns a timetable for the given city as a dictionary
    #  - keys are names of possible end stations
    #  - values are lists of departure times as tuples (hour, minute)
    #    regardless of the concrete line that goes there
    timetable = {}

    for line in line_infos.values():
        end_city = line[-1][0]
        first_city = line[0][0]

        city_found = False
        for station_name, time_info in line:
            if station_name == city:
                city_found = True
                break

        if not city_found:  
            continue
        
        if end_city not in timetable:
            timetable[end_city] = []
        
        if station_name == first_city:
            timetable[end_city].extend(line[0][1])
        else:
            departure_times = []
            minutes_count = 0
            stops_count = 0  
            

            for station_name, time in line: 
                if station_name == first_city:
                    continue
                minutes_count += time
                stops_count += 1  
                if station_name == city:
                    break
            
            minutes_count += stops_count
            
            for total_hours, total_minutes in line[0][1]:
                total_minutes += minutes_count % 60
                total_hours += minutes_count // 60
                if total_minutes >= 60:
                    total_minutes %= 60
                    total_hours += 1
            
                departure_times.append((total_hours, total_minutes))

            timetable[end_city].extend(departure_times)
        
    for end_city in timetable:
        timetable[end_city].sort()

    return timetable
    


def load_arrival_times(path, line_infos):  # 2
    # the function loads real arrival data from a file
    # inputs:
    #  - path: path to a csv file with real arrival and departure times
    #  - line_infos: dictionary with timetable (as loaded by load_line_infos)
    # the function returns a dictionary with the following structure:
    #  - keys are line numbers (integers)
    #  - values are dictionaries:
    #     - keys are scheduled departure times (tuple of two ints)
    #     - values are dictionaries:
    #         - values are dates (string format: YYYY-MM-DD)
    #         - values are lists with tuples
    #           each tuple has four values:
    #            - city name (string - one tuple for each stop)
    #            - scheduled arrival (tuple (hour, minute))
    #            - real arrival (tuple (hour, minute))
    #            - delay in minutes (int - always round down)

    scheduled_time = {}

    for line_num, xline in line_infos.items():
                scheduled_time[line_num] = {}
                for dep_time in xline[0][1]: 
                    scheduled_time[line_num][dep_time] = {}

    with open(path, "r", encoding="utf-8") as my_file:
        for line in my_file:
            my_line = line.rstrip().split(",")
            line_num, city, date_time, event = my_line
            line_num = int(line_num)
            my_date, time_str = date_time.split(" ")
            hour, minute, _ = map(int, time_str.split(":"))
            time = (hour, minute)

            if line_num not in line_infos:
                continue

            values = line_infos[line_num]

            

        
            #if line_num == 398:
            #    print(line_num, city, my_date, time, event)
        """   
            if line_num not in line_infos:
                continue

            values = line_infos[line_num]
            next_stop_list = []

            #


            if line_num in line_infos:
                for i, (next_stop, x) in enumerate(values):
                    if i != 0 and next_stop not in next_stop_list:

                        next_stop_tuple = (next_stop,(), dep_time, random.randint(1, 5))
                        next_stop_list.append(next_stop_tuple) 
                        


            for dep_time in scheduled_time[line_num]:
                scheduled_time[line_num][dep_time][my_date] = next_stop_list
           
             """
    
   
    return scheduled_time


def get_most_delayed_line(loaded_arrivals):  # 1
    # finds the line that accrued the most delays on average on the final stop
    # input:
    #  - loaded_arrivals: dictionary with arrival information
    #    (as loaded by load_arrival_times)
    # output:
    #  - tuple of two values:
    #    - line number (int)
    #    - average delay in minutes (float)
    
    highest_key = None
    highest_average = 0

    for key, dict in loaded_arrivals.items():
        total_delay = 0
        counter = 0
        for _, line in dict.items():
            for _, cities in line.items():
                if cities: 
                    final_stop = cities[-1]
                    delay = final_stop[-1]
                    if isinstance(delay, (int, float)):
                        total_delay += delay
                        counter += 1


        if counter > 0:
            average = total_delay / counter
            if average >= highest_average:
                highest_average = average
                highest_key = key
        #print(f"key: {key}, | sum: {delay} | counter: {counter} | average: {average}")
    
    return (highest_key, highest_average) if highest_key is not None else (None, 0)


def get_most_delayed_city(loaded_arrivals):  # 1
    # finds the city where trains arrive with the most delay on average
    # input:
    #  - loaded_arrivals: dictionary with arrival information
    #    (as loaded by load_arrival_times)
    # output:
    #  - tuple of two values:
    #    - city name (string)
    #    - average delay in minutes (float)
    city_dict = {}

    for key, dict in loaded_arrivals.items():
        total_delay = 0
        counter = 0
        for time_key, line in dict.items():
            for date_key, cities in line.items():
                for city in cities:
                    city_name = city[0]
                    delay = city[-1]
                    if city_name not in city_dict:
                        city_dict[city_name] = {'total_delay': 0, 'count': 0}
                    city_dict[city_name]['total_delay'] += delay
                    city_dict[city_name]['count'] += 1
                    
    highest_city = None
    highest_average = 0      
    for city_name, data in city_dict.items():
        average = city_dict[city_name]['total_delay'] / city_dict[city_name]['count']
        if average >= highest_average:
            highest_average = average
            highest_city = city_name
    
    return (highest_city, highest_average) if highest_city is not None else (None, 0)


if __name__ == '__main__':
    # test your functions here

    
    path = os.path.join(os.path.dirname(__file__), "timetable.csv")
    data = load_line_infos(path)
    
    for key, value in data.items():
        print(f"{key} : {value}") 
    
    
    """  
    line_infos = {12: [("Bratislava", [(6, 30), (7, 45), (9, 0)]), ("Trnava",35), ("Nitra", 50), ("Zvolen", 60)]}
    print(find_next_train(line_infos, 12, 7, 31))
    """

    
    """ line_infos = {
        12: [('Bratislava', (10, 30)), ('Trnava', (7, 15)), ('Košice', (12, 10))],
        13: [('Bratislava', (8, 45)), ('Trnava', (10, 20)), ('Zvolen', (11, 50))],
        14: [('Bratislava', (9, 10)), ('Košice', (14, 30))],
        15: [('Kosice', (9, 10)), ('Trnava', (14, 30))],
    } """

    
    print(get_city_timetable(data, "FEA")) 
    
    """ 
    path2 = os.path.join(os.path.dirname(__file__), "arrivals.csv")
    #data = {920: [('KGK', [(6, 10), (9, 45), (12, 20)]), ('GLG', 6), ('MGJ', 2), ('IGP', 8), ('PBA', 9), ('CCZ', 3), ('KOM', 4), ('EXE', 5), ('JND', 1), ('QKM', 3), ('UAO', 7), ('NKX', 8), ('NGK', 3)]}
    loaded_arrivals = load_arrival_times(path2, data)
    print(loaded_arrivals)
     """

    #print(get_most_delayed_line(loaded_arrivals))
    #print(get_most_delayed_city(loaded_arrivals))
    