import random
import string

import employee as emp
from config import SENIORITY, WAGES


def get_random_letter(letters):
    return random.choice(letters)


def generate_name(n):
    name = get_random_letter(string.ascii_uppercase)
    for _ in range(n - 1):
        name += get_random_letter(string.ascii_lowercase)
    return name


def test_structure(obj, should_have):
    attribute_list = dir(obj)
    for att in should_have:
        if att not in attribute_list:
            print(f"\tMissing attribute {att} in object {obj}. (Found attributes {attribute_list})")
    else:
        return True
    return False


def test_employee_errors():
    points = 0.0

    # check for bad seniority - 0.5 points
    test_sen = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
    while test_sen in SENIORITY:
        test_sen = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))

    try:
        test_emp = emp.Employee("Janko Hrasko", test_sen, 15.45)
    except ValueError as val_e:
        if str(val_e) == f"Unknown seniority level {test_sen}":
            points += 0.5
        else:
            print(f"\tCalling Employee constructor with invalid seniority caused an error with wrong message")
            print(f"\tExpected 'Unknown seniority level {test_sen}', got {str(val_e)}")
    except Exception as e:
        print("\tCalling Employee with invalid seniority caused error with wrong type")
        print(f"\tExpected ValueError, got {type(e)}")
    else:
        print("\tCalling Employee with invalid seniority should cause an error, no error was generated")

    # check for non-number wage - 0.25 points
    test_wage = "23.45"

    try:
        test_emp = emp.Employee("Janko Hrasko", "medior", test_wage)
    except TypeError as type_e:
        expected = f"Incorrect wage type: {type(test_wage)}"
        if str(type_e) == expected:
            points += 0.25
        else:
            print(f"\tCalling Employee constructor with invalid wage type caused an error with wrong message")
            print(f"\tExpected {expected}, got {str(type_e)}")
    except Exception as e:
        print("\tCalling Employee with invalid wage type caused error with wrong type")
        print(f"\tExpected TypeError, got {type(e)}")
    else:
        print("\tCalling Employee with invalid wage type should cause an error, no error was generated")


    # check for invalid wage - 0.25 points
    test_wage = round(random.uniform(-WAGES["medior"][1], -WAGES["medior"][0]), 2)

    try:
        test_emp = emp.Employee("Janko Hrasko", "medior", test_wage)
    except ValueError as val_e:
        expected = f"Incorrect wage for medior worker: {test_wage}"
        if str(val_e) == expected:
            points += 0.25
        else:
            print(f"\tCalling Employee constructor with invalid wage value caused an error with wrong message")
            print(f"\tExpected {expected}, got {str(type_e)}")
    except Exception as e:
        print("\tCalling Employee with invalid wage value caused error with wrong type")
        print(f"\tExpected ValueError, got {type(e)}")
    else:
        print("\tCalling Employee with invalid wage value should cause an error, no error was generated")

    return points


def test_employee():
    print("Testing Employee constructor...")
    points = 0.0
    test_name = generate_name(5) + ' ' + generate_name(8)
    test_level = random.choice(SENIORITY)
    test_pay = round(random.uniform(WAGES[test_level][0], WAGES[test_level][1]), 2)

    try:
        test_emp = emp.Employee(test_name, test_level, test_pay)
    except Exception as e:
        print("\tCalling Employee constructor caused an unexpected error:")
        print(e)
    else:
        if test_structure(test_emp, ['name', 'level', 'wage', 'curr_project']):
            points = test_employee_errors()

            if test_emp.curr_project is not None:
                print(f"\tEmployee.curr_project should be None, found {test_emp.curr_project}")
                points = 0.0
            if test_emp.name != test_name:
                print(f"\tEmployee.name should be {test_name}, found {test_emp.name}")
                points = 0.0
            if test_emp.level != test_level:
                print(f"\tEmployee.level should be {test_level}, found {test_emp.level}")
                points = 0.0
            if abs(test_emp.wage - test_pay) > 0.01:
                print(f"\tEmployee.wage should be {test_pay}, found {test_emp.wage}")
                points = 0.0
    
    print(f"Testing Employee constructor finished: {points:.2f}/1 point")
    return points


def test_tester():
    print("Testing Tester constructor...")
    points = 0.0
    test_name = generate_name(5) + ' ' + generate_name(8)
    test_level = random.choice(SENIORITY)
    test_pay = round(random.uniform(WAGES[test_level][0], WAGES[test_level][1]), 2)

    try:
        test_emp = emp.Tester(test_name, test_level, test_pay)
    except Exception as e:
        print("\tCalling Tester constructor caused an unexpected error:")
        print(e)
    else:
        if test_structure(test_emp, ['name', 'level', 'wage', 'curr_project']):
            if (isinstance(test_emp, emp.Employee)):
                points += 0.2
                if test_emp.curr_project is not None:
                    print(f"\tTester.curr_project should be None, found {test_emp.curr_project}")
                    points = 0.0
                if test_emp.name != test_name:
                    print(f"\tTester.name should be {test_name}, found {test_emp.name}")
                    points = 0.0
                if test_emp.level != test_level:
                    print(f"\tTester.level should be {test_level}, found {test_emp.level}")
                    points = 0.0
                if abs(test_emp.wage - test_pay) > 0.01:
                    print(f"\tTester.wage should be {test_pay}, found {test_emp.wage}")
                    points = 0.0
            else:
                print("\tTester should inherit from Employee")
    
    print(f"Testing Tester constructor finished: {points:.2f}/0.2 points")
    return points


def test_developer():
    print("Testing Developer constructor...")
    points = 0.0
    test_name = generate_name(5) + ' ' + generate_name(8)
    test_level = random.choice(SENIORITY)
    test_pay = round(random.uniform(WAGES[test_level][0], WAGES[test_level][1]), 2)
    test_langs = [
        ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        for i in range(3)
    ]

    try:
        test_emp = emp.Developer(test_name, test_level, test_pay, test_langs)
    except Exception as e:
        print("\tCalling Developer constructor caused an unexpected error:")
        print(e)
    else:
        if test_structure(test_emp, ['name', 'level', 'wage', 'curr_project', 'languages']):
            if (isinstance(test_emp, emp.Employee)):
                points += 0.3
                if test_emp.curr_project is not None:
                    print(f"\tDeveloper.curr_project should be None, found {test_emp.curr_project}")
                    points = 0.0
                if test_emp.name != test_name:
                    print(f"\tDeveloper.name should be {test_name}, found {test_emp.name}")
                    points = 0.0
                if test_emp.level != test_level:
                    print(f"\tDeveloper.level should be {test_level}, found {test_emp.level}")
                    points = 0.0
                if test_emp.languages != test_langs:
                    print(f"\tDeveloper.languages should be {test_langs}, found {test_emp.languages}")
                    points = 0.0
                if abs(test_emp.wage - test_pay) > 0.01:
                    print(f"\tDeveloper.wage should be {test_pay}, found {test_emp.wage}")
                    points = 0.0
            else:
                print("\tDeveloper should inherit from Employee")
    
    print(f"Testing Developer constructor finished: {points:.2f}/0.3 points")
    return points


def test_manager_constructor():
    print("Testing Manager constructor...")
    points = 0.0
    test_name = generate_name(5) + ' ' + generate_name(8)
    test_level = random.choice(SENIORITY)
    test_pay = round(random.uniform(WAGES[test_level][0], WAGES[test_level][1]), 2)

    try:
        test_emp = emp.Manager(test_name, test_level, test_pay)
    except Exception as e:
        print("\tCalling Manager constructor caused an unexpected error:")
        print(e)
    else:
        if test_structure(test_emp, ['name', 'level', 'wage', 'curr_project']):
            if (isinstance(test_emp, emp.Employee)):
                points += 0.2
                if test_emp.curr_project is not None:
                    print(f"\tManager.curr_project should be None, found {test_emp.curr_project}")
                    points = 0.0
                if test_emp.name != test_name:
                    print(f"\tManager.name should be {test_name}, found {test_emp.name}")
                    points = 0.0
                if test_emp.level != test_level:
                    print(f"\tManager.level should be {test_level}, found {test_emp.level}")
                    points = 0.0
                if abs(test_emp.wage - test_pay) > 0.01:
                    print(f"\tManager.wage should be {test_pay}, found {test_emp.wage}")
                    points = 0.0
            else:
                print("\tManager should inherit from Employee")
    
    print(f"Testing Manager constructor finished: {points:.2f}/0.2 points")
    return points


def test_manager_get_project_time():
    print("Testing Manager.get_project_time()...")
    points = 0.0
    test_cases = [
        ('junior', 10, 12), ('junior', 20, 24), ('junior', 50, 60), ('junior', 17, 21), ('junior', 134, 161),
        ('medior', 10, 10), ('medior', 20, 20), ('medior', 50, 50), ('medior', 17, 17), ('medior', 134, 134),
        ('senior', 10, 8), ('senior', 20, 16), ('senior', 50, 40), ('senior', 17, 14), ('senior', 134, 108),
    ]
    test_name = generate_name(5) + ' ' + generate_name(8)

    for level, orig, res in  test_cases:
        test_pay = round(random.uniform(WAGES[level][0], WAGES[level][1]), 2)
        test_emp = emp.Manager(test_name, level, test_pay)

        try:
            st_res = test_emp.get_project_time(orig)
        except Exception as e:
            print("\tCalling Manager.get_project_time() caused an unexpected error")
            print(e)
        else:
            if st_res == res:
                points += 0.02
            else:
                print(f"\tManager.get_project_time() returned wrong value: Result should be {res} with {level} manager and {orig} original time, got {st_res}")

    print(f"Testing Manager.get_project_time() finished: {points:.2f}/0.3 points")
    return points


def test_manager():
    print("Testing Manager...")
    points = test_manager_constructor()
    points += test_manager_get_project_time()
    print(f"Testing Manager finished: {points:.2f}/0.5 points")
    return points


def main():
    emp_points = test_employee()
    print()
    tester_points = test_tester()
    print()
    developer_points = test_developer()
    print()
    manager_points = test_manager()
    print()

    print(f"EMPLOYEE points: {emp_points:.2f}/1 point")
    print(f"TESTER points: {tester_points:.2f}/0.2 points")
    print(f"DEVELOPER points: {developer_points:.2f}/0.3 points")
    print(f"MANAGER points: {manager_points:.2f}/0.5 points")


if __name__ == '__main__':
    main()
