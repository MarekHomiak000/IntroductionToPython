import pickle
import random


import assignment1 as st_solution


def test_load_line_infos():
    print("Testing load_line_infos()...")
    points = 0

    with open("line_infos.pkl", 'rb') as in_file:
        test_cases = pickle.load(in_file)

    types_correct = True
    for path, correct in random.sample(test_cases, 15):
        try:
            st_res = st_solution.load_line_infos(path)
        except Exception as e:
            print("Calling load_line_infos() caused an error:")
            print(e)
            types_correct = False
            continue

        if not isinstance(st_res, dict):
            print(f"\tload_line_infos() returned wrong type: expected dict, got {type(st_res)}")
            types_correct = False
            continue

        corr_count = len(set(correct.keys()))
        st_count = len(set(st_res.keys()))
        if st_count != corr_count:
            print(f"\tload_line_infos() returned wrong value: expected dict with {corr_count} values, got {st_count}")
            print(f"\tExpected: {set(correct.keys())}")
            print(f"\tGot: {set(st_res.keys())}")
            continue

        values_ok = True
        for line_no in st_res:
            if not isinstance(line_no, int):
                print(f"\tload_line_infos() returned wrong type: dict keys should be integers, got {type(line_no)}")
                types_correct = False
                continue

            if line_no not in correct:
                print(f"\tload_line_infos() loaded unexpected line {line_no}")
                values_ok = False
                continue

            st_info = st_res[line_no]
            corr_info = correct[line_no]
            if not isinstance(st_info, list):
                print(f"\tload_line_infos() returned wrong type: dict values should be lists, got {type(line_no)}")
                types_correct = False
                continue

            if len(st_info) != len(corr_info):
                print(f"\tWrong information loaded for line {line_no}: expected {len(corr_info)} stops, got {len(st_info)}")
                print(f"\tExpected: {corr_info}")
                print(f"\tGot: {st_info}")
                values_ok = False
                continue

            corr_stops = [city for city, _ in corr_info]
            for idx, elem in enumerate(st_info):
                if not isinstance(elem, tuple):
                    print(f"\tload_line_infos() returned wrong type: stop information should be tuple, got {type(elem)}")
                    print(f"\tFor element: {elem} (line number {line_no})")
                    types_correct = False
                    values_ok = False
                    break

                if len(elem) != 2:
                    print(f"\tload_line_infos() returned wrong value: stop information should be tuple of 2 values, got {len(elem)}")
                    print(f"\tFor element: {elem} (line number {line_no})")
                    values_ok = False
                    break

                city, further = elem
                if not isinstance(city, str):
                    print(f"\tload_line_infos() returned wrong type: stop name should be string, got {type(city)}")
                    print(f"\tFor element: {elem} -> {city}")
                    types_correct = False
                    values_ok = False
                    break

                if city not in corr_stops:
                    print(f"\tload_line_infos() returned wrong value (line {line_no}): {city} is not a valid stop")
                    print(f"\tExpected stop: {corr_stops}")
                    values_ok = False
                    break

                corr_city, corr_value = corr_info[idx]
                if city != corr_city:
                    print(f"\tload_line_infos() returned wrong value (line {line_no}): stop at {idx} should be {corr_city}, got {city}")
                    values_ok = False
                    break

                if idx == 0:
                    if not isinstance(further, list):
                        print(f"\tload_line_infos() returned wrong type (line {line_no}): stop info for first stop should be list, got {type(further)}")
                        print(f"\tFor element: {further}")
                        types_correct = False
                        values_ok = False
                        break

                    for time in further:
                        if not isinstance(time, tuple):
                            print(f"\tload_line_infos() returned wrong type (line {line_no}): stop info for first stop should be list of tuples, got {type(time)}")
                            print(f"\tFor element: {time} in {further}")
                            types_correct = False
                            values_ok = False
                            break

                        if len(time) != 2:
                            print(f"\tload_line_infos() returned wrong value: stop info for first stop should contain tuples of 2 values, got {len(time)}")
                            print(f"\tFor element: {time} in {further}")
                            values_ok = False
                            break

                        if not isinstance(time[0], int) or not isinstance(time[1], int):
                            print(f"\tload_line_infos() returned wrong type (line {line_no}): stop info for first stop should be list of tuples with two integers, got ({type(time[0])}, {type(time[1])})")
                            print(f"\tFor element: {time} in {further}")
                            types_correct = False
                            values_ok = False
                            break
                else:
                    if not isinstance(further, int):
                        print(f"\tload_line_infos() returned wrong type (line {line_no}): stop info for later stops should be int, got {type(further)}")
                        types_correct = False
                        values_ok = False
                        break

                if further != corr_value:
                    print(f"\tload_line_infos() returned wrong value (line {line_no}) for stop at {idx}: {city}")
                    print(f"\tExpected: {corr_value}")
                    print(f"\tGot: {further}")
                    values_ok = False
                    break

        if types_correct and values_ok:
            points += 0.1

    if types_correct and points > 0.5:
        points += 0.5

    print(f"Testing load_line_infos() finished: {points:.2f}/2 points")
    return points


def test_find_next_train():
    print("Testing find_next_train()...")
    points = 0

    with open("next_train.pkl", 'rb') as in_file:
        test_cases = pickle.load(in_file)

    types_correct = True
    cities_ok = True
    correct_count = 0
    for inputs, correct in test_cases:
        values_ok = True
        infos, line_no, hour, minute = inputs
        try:
            st_res = st_solution.find_next_train(infos, line_no, hour, minute)
        except Exception as e:
            print("Calling find_next_train() caused an error:")
            print(e)
            types_correct = False
            continue

        if not isinstance(st_res, list):
            print(f"\tfind_next_train() returned wrong type: expected list, got {type(st_res)}")
            print(f"\tFor result: {st_res}")
            types_correct = False
            continue

        st_count = len(st_res)
        corr_count = len(correct)
        if st_count != corr_count:
            print(f"\tfind_next_train() returned wrong value: expected {corr_count} stops, got {st_count}")
            print(f"\tExpected: {correct}")
            print(f"\tGot: {st_res}")
            values_ok = False
            continue

        for idx, elem in enumerate(st_res):
            if not isinstance(elem, tuple):
                print(f"\tfind_next_train() returned wrong type: expected list of tuples, found {type(elem)}")
                print(f"\tFor element {elem} in {st_res}")
                types_correct = False
                values_ok = False
                break

            if len(elem) != 2:
                print(f"\tfind_next_train() returned wrong value: stop information should be tuple of 2 values, got {len(elem)}")
                print(f"\tFor element: {elem} in {st_res}")
                values_ok = False
                break

            st_city, st_time = elem
            if not isinstance(st_city, str):
                print(f"\tfind_next_train() returned wrong type: stop name should be string, got {type(st_city)}")
                print(f"\tFor element: {elem} -> {st_city}")
                types_correct = False
                values_ok = False
                break

            if not isinstance(st_time, tuple):
                print(f"\tfind_next_train() returned wrong type: stop time should be tuple, got {type(st_time)}")
                print(f"\tFor element: {st_time} in {elem}")
                types_correct = False
                values_ok = False
                break

            if len(st_time) != 2:
                print(f"\tfind_next_train() returned wrong value: stop time should be tuple of 2 values, got {len(st_time)}")
                print(f"\tFor element: {st_time} in {elem}")
                values_ok = False
                break

            if not isinstance(st_time[0], int) or not isinstance(st_time[1], int):
                print(f"\tfind_next_train() returned wrong type (line {line_no}): stop time should be a tuple with two integers, got ({type(st_time[0])}, {type(st_time[1])})")
                print(f"\tFor element: {st_time} in {elem}")
                types_correct = False
                values_ok = False
                break

            corr_city, corr_time = correct[idx]
            if st_city != corr_city:
                print(f"\tfind_next_train() returned wrong value: stop at {idx} should be {corr_city}, got {st_city}")
                values_ok = False
                break

            if st_time != corr_time:
                print(f"\tfind_next_train() returned wrong value: stop at {idx} should be at time {corr_time}, got {st_time}")
                values_ok = False
                break

        correct_count += values_ok

    points = (correct_count / len(test_cases)) * 0.5
    orig_points = points
    if types_correct and orig_points > 0.25:  # half the results must be correct to get points for types
        points += 0.2
    if cities_ok and orig_points > 0.25:
        points += 0.3

    print(f"Testing find_next_train() finished: {points:.2f}/1 point")
    return points


def test_get_city_timetable():
    print("Testing get_city_timetable()...")
    points = 0

    with open("city_timetable.pkl", 'rb') as in_file:
        test_cases = pickle.load(in_file)

    cities_count = 0
    times_count = 0
    for inputs, correct in test_cases:
        infos, city = inputs
        try:
            st_res = st_solution.get_city_timetable(infos, city)
        except Exception as e:
            print("Calling get_city_timetable() caused an error:")
            print(e)
            continue

        if not isinstance(st_res, dict):
            print(f"\tget_city_timetable() returned wrong type: expected dict, got {type(st_res)}")
            continue

        corr_count = len(correct)
        st_count = len(st_res)
        if st_count != corr_count:
            print(f"\tget_city_timetable() returned wrong value: expected dict with {corr_count} keys, got {st_count}")
            print(f"\tExpected: {set(correct.keys())}")
            print(f"\tGot: {set(st_res.keys())}")
            continue

        all_times = True
        for city in st_res:
            if city not in correct:
                print(f"\tget_city_timetable() returned unexpected destination {city}")
                print(f"\tExpected: {set(correct.keys())}")
                print(f"\tGot: {set(st_res.keys())}")
                break

            if not isinstance(st_res[city], list):
                print(f"\tget_city_timetable() returned wrong type: information for city should be list, got {type(st_res[city])}")
                continue

            for time in correct[city]:
                if time not in st_res[city]:
                    print(f"\tget_city_timetable() returned wrong value: start time {time} missing")
                    print(f"\tExpected: {correct[city]}")
                    print(f"\tGot: {st_res[city]}")
                    all_times = False
                    break
        else:
            cities_count += 1
            times_count += all_times

    points += (cities_count / len(test_cases))
    points += (times_count / len(test_cases))

    print(f"Testing get_city_timetable() finished: {points:.2f}/2 points")
    return points


def test_load_arrival_times():
    print("Testing load_arrival_times()...")
    points = 0

    types_correct = True

    with open("arrival_times.pkl", 'rb') as in_file:
        test_cases = pickle.load(in_file)

    for inputs, correct in random.sample(test_cases, 5):
        values_loaded = True
        values_correct = True
        path, infos = inputs
        try:
            st_res = st_solution.load_arrival_times(path, infos)
        except Exception as e:
            print("Calling load_arrival_times() caused an error:")
            print(e)
            types_correct = False
            continue

        if not isinstance(st_res, dict):
            print(f"\tload_arrival_times() returned wrong type: expected dict, got {type(st_res)}")
            types_correct = False
            continue

        corr_count = len(set(correct.keys()))
        st_count = len(set(st_res.keys()))
        if st_count != corr_count:
            print(f"\tload_arrival_times() returned wrong value: expected dict with {corr_count} values, got {st_count}")
            print(f"\tExpected: {set(correct.keys())}")
            print(f"\tGot: {set(st_res.keys())}")
            values_loaded = False
            values_correct = False
            continue

        for line_no in st_res:
            if not isinstance(line_no, int):
                print(f"\tload_arrival_times() returned wrong type: line number should be int, got {type(line_no)}")
                types_correct = False
                values_loaded = False
                values_correct = False
                break

            if line_no not in correct:
                print(f"\tload_arrival_times() returned wrong value: unexpected line {line_no}")
                print(f"\tExpected: {set(correct.keys())}")
                values_loaded = False
                values_correct = False
                break

            line_info = st_res[line_no]
            corr_info = correct[line_no]
            if not isinstance(line_info, dict):
                print(f"\tload_arrival_times() returned wrong type: line information {line_no} should be dict, got {type(line_info)}")
                types_correct = False
                values_loaded = False
                values_correct = False
                break

            corr_l_count = len(set(corr_info.keys()))
            st_l_count = len(set(line_info.keys()))
            if st_l_count != corr_l_count:
                print(f"\tload_arrival_times() returned wrong value: line {line_no} should have {corr_l_count} start times, got {st_l_count}")
                print(f"\tExpected: {set(corr_info.keys())}")
                print(f"\tGot: {set(line_info.keys())}")
                values_loaded = False
                values_correct = False
                break

            for start_time in line_info:
                if not isinstance(start_time, tuple):
                    print(f"\tload_arrival_times() returned wrong type: start times should be tuples, got {type(start_time)} (line {line_no})")
                    types_correct = False
                    values_loaded = False
                    values_correct = False
                    break

                if not isinstance(start_time[0], int) or not isinstance(start_time[1], int):
                    print(f"\tload_arrival_times() returned wrong type (line {line_no}): start time should be tuple of ints, got ({type(start_time[0])}, {type(start_time[1])})")
                    print(f"\tFor element: {start_time}")
                    types_correct = False
                    values_loaded = False
                    values_correct = False
                    break

                if start_time not in corr_info:
                    print(f"\tload_arrival_times() returned wrong value: unexpected start time {start_time} for line {line_no}")
                    print(f"\tExpected: {set(corr_info.keys())}")
                    values_loaded = False
                    values_correct = False
                    break

                st_dates = line_info[start_time]
                corr_dates = corr_info[start_time]
                corr_d_count = len(set(corr_dates.keys()))
                st_d_count = len(set(st_dates.keys()))
                if st_d_count != corr_d_count:
                    print(f"\tload_arrival_times() returned wrong value: line {line_no} at {start_time} should have {corr_d_count} dates, got {st_d_count}")
                    print(f"\tExpected: {set(corr_dates.keys())}")
                    print(f"\tGot: {set(st_dates.keys())}")
                    values_loaded = False
                    values_correct = False
                    break

                for st_date in st_dates:
                    if not isinstance(st_date, str):
                        print(f"\tload_arrival_times() returned wrong type: dates should be strings, got {type(st_date)} (line {line_no}, start time {start_time})")
                        types_correct = False
                        values_loaded = False
                        values_correct = False
                        break

                    if st_date not in corr_dates:
                        print(f"\tload_arrival_times() returned wrong value: unexpected date {st_date} for line {line_no}, start time {start_time}")
                        print(f"\tExpected: {set(corr_dates.keys())}")
                        values_loaded = False
                        values_correct = False
                        break

                    # under each date we should have a list of city infos
                    st_d_delays = st_dates[st_date]
                    corr_d_delays = corr_dates[st_date]
                    if not isinstance(st_d_delays, list):
                        print(f"\tload_arrival_times() returned wrong type: delay info for a date should be list, got {type(st_d_delays)}")
                        types_correct = False
                        values_loaded = False
                        values_correct = False
                        break

                    # check number of stops
                    st_stops = len(st_d_delays)
                    corr_stops = len(corr_d_delays)
                    if st_stops != corr_stops:
                        print(f"\tload_arrival_times() returned wrong value: expected {corr_stops} for line {line_no}, got {st_stops}")
                        values_loaded = False
                        values_correct = False

                    # city info should be tuple: string, tuple of ints, tuple of ints, int
                    for st_c_info in st_d_delays:
                        if not isinstance(st_c_info, tuple):
                            print(f"\tload_arrival_times() returned wrong type: city delay information should be tuple, got {type(st_c_info)} (line {line_no}, start time {start_time}, date {st_date})")
                            types_correct = False
                            values_loaded = False
                            values_correct = False
                            break

                        if len(st_c_info) != 4:
                            print(f"\tload_arrival_times() returned wrong value: city delay information should be tuple of 4, got {len(st_c_info)} (line {line_no}, start time {start_time}, date {st_date})")
                            types_correct = False
                            values_loaded = False
                            values_correct = False
                            break

                        city, expected, real, delay = st_c_info
                        if not isinstance(city, str):
                            print(f"\tload_arrival_times() returned wrong type: city name should be string, got {type(city)} (line {line_no}, start time {start_time}, date {st_date})")
                            types_correct = False
                            values_loaded = False
                            values_correct = False
                            break

                        if not isinstance(expected, tuple):
                            print(f"\tload_arrival_times() returned wrong type: expected time should be tuple, got {type(expected)} (line {line_no}, start time {start_time}, date {st_date})")
                            types_correct = False
                            values_loaded = False
                            values_correct = False
                            break

                        if not isinstance(real, tuple):
                            print(f"\tload_arrival_times() returned wrong type: arrival time should be tuple, got {type(real)} (line {line_no}, start time {start_time}, date {st_date})")
                            types_correct = False
                            values_loaded = False
                            values_correct = False
                            break

                        if not isinstance(delay, int):
                            print(f"\tload_arrival_times() returned wrong type: delay information should be int, got {type(delay)} (line {line_no}, start time {start_time}, date {st_date})")
                            types_correct = False
                            values_loaded = False
                            values_correct = False
                            break

                        # city info should be in correct
                        if st_c_info not in corr_d_delays:
                            print(f"\tload_arrival_times() returned wrong value: unexpected city delay information {st_c_info} (line {line_no}, start time {start_time}, date {st_date})")
                            print(f"\tExpected: {corr_d_delays}")
                            print(f"\tGot: {st_d_delays}")
                            values_correct = False
                            break

        points += values_loaded * 0.1
        points += values_correct * 0.2

    if points > 0 and types_correct:
        points += 0.5

    print(f"Testing load_arrival_times() finished: {points:.2f}/2 points")
    return points


def test_get_most_delayed_line():
    print("Testing get_most_delayed_line()...")
    points = 0

    with open("delayed_line.pkl", 'rb') as in_file:
        test_cases = pickle.load(in_file)

    correct_count = 0
    for loaded_arrivals, correct in test_cases:
        try:
            st_res = st_solution.get_most_delayed_line(loaded_arrivals)
        except Exception as e:
            print("\tCalling get_most_delayed_line() caused an error:")
            print(f"\t{e}")
            continue

        if not isinstance(st_res, tuple):
            print(f"\tget_most_delayed_line() returned wrong type: expected tuple, got {type(st_res)}")
            continue

        if len(st_res) != 2:
            print(f"\tget_most_delayed_line() returned wrong value: expected tuple with two values, got {len(st_res)}")
            continue

        line, avg_delay = st_res
        if not isinstance(line, int):
            print(f"\tget_most_delayed_line() returned wrong type: line number should be int, got {type(line)}")
            continue

        if not isinstance(avg_delay, float):
            print(f"\tget_most_delayed_line() returned wrong type: average delay should be float, got {type(avg_delay)}")
            continue

        corr_line, corr_delay = correct
        if line != corr_line:
            print(f"\tget_most_delayed_line() returned wrong value: expected line {corr_line}, got {line}")
            continue

        if abs(corr_delay - avg_delay) > 0.001:
            print(f"\tget_most_delayed_line() returned wrong value: expected average delay {corr_delay:.4f}, got {avg_delay:.4f}")
            continue

        correct_count += 1

    points = correct_count / len(test_cases)

    print(f"Testing get_most_delayed_line() finished: {points:.2f}/1 point")
    return points


def test_get_most_delayed_city():
    print("Testing get_most_delayed_city()...")
    points = 0

    with open("delayed_city.pkl", 'rb') as in_file:
        test_cases = pickle.load(in_file)

    correct_count = 0
    for loaded_arrivals, correct in test_cases:
        try:
            st_res = st_solution.get_most_delayed_city(loaded_arrivals)
        except Exception as e:
            print("\tCalling get_most_delayed_city() caused an error:")
            print(f"\t{e}")
            continue

        if not isinstance(st_res, tuple):
            print(f"\tget_most_delayed_city() returned wrong type: expected tuple, got {type(st_res)}")
            continue

        if len(st_res) != 2:
            print(f"\tget_most_delayed_city() returned wrong value: expected tuple with two values, got {len(st_res)}")
            continue

        city, avg_delay = st_res
        if not isinstance(city, str):
            print(f"\tget_most_delayed_city() returned wrong type: city number should be string, got {type(city)}")
            continue

        if not isinstance(avg_delay, float):
            print(f"\tget_most_delayed_city() returned wrong type: average delay should be float, got {type(avg_delay)}")
            continue

        corr_city, corr_delay = correct
        if city != corr_city:
            print(f"\tget_most_delayed_city() returned wrong value: expected city {corr_city}, got {city}")
            continue

        if abs(corr_delay - avg_delay) > 0.001:
            print(f"\tget_most_delayed_city() returned wrong value: expected average delay {corr_delay:.4f}, got {avg_delay:.4f}")
            continue

        correct_count += 1

    points = correct_count / len(test_cases)

    print(f"Testing get_most_delayed_city() finished: {points:.2f}/1 point")
    return points


def main():
    p1 = test_load_line_infos()
    print()
    p2 = test_find_next_train()
    print()
    p3 = test_get_city_timetable()
    print()
    p4 = test_load_arrival_times()
    print()
    p5 = test_get_most_delayed_line()
    print()
    p6 = test_get_most_delayed_city()
    print()

    total = sum([p1, p2, p3, p4, p5, p6])
    if total >= 5:
        print("Extra point given")
        total += 1

    print(f"TOTAL POINTS: {total:.2f}/10")


if __name__ == '__main__':
    main()
