import random
import string

import order as st_ord


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


def test_order_constructor():
    print("Testing Order constructor...")
    points = 0.0

    test_client = generate_name(10)
    test_offer = random.randint(100, 1000) * 10
    test_active = random.randint(1, 100)
    test_total_hours = random.randint(50, 200)

    try:
        test_order = st_ord.Order(test_client, test_offer, test_active, test_total_hours)
    except Exception as e:
        print("\tCalling Order constructor caused an unexpected error:")
        print(e)
    else:
        if test_structure(test_order,
                          ['client', 'offer', 'active', 'total_hours', 'stages', 'required_technologies']):
            points = 0.1

            if test_order.client != test_client:
                print(f"\tOrder.client should be {test_client}, found {test_order.client}")
                points = 0.0
            if test_order.offer != test_offer:
                print(f"\tOrder.offer should be {test_offer}, found {test_order.offer}")
                points = 0.0
            if test_order.active != test_active:
                print(f"\tOrder.active should be {test_active}, found {test_order.active}")
                points = 0.0
            if test_order.total_hours != test_total_hours:
                print(f"\tOrder.total_hours should be {test_total_hours}, found {test_order.total_hours}")
                points = 0.0
            if not isinstance(test_order.stages, dict):
                print(f"\tOrder.stages should be a dictionary, found {type(test_order.stages)}")
                points = 0.0
            if len(test_order.stages) != 0:
                print(f"\tOrder.stages should be empty, found {len(test_order.stages)} keys")
                points = 0.0
            if not isinstance(test_order.required_technologies, list):
                print(f"\tOrder.required_technologies should be a list, found {type(test_order.required_technologies)}")
                points = 0.0
            if len(test_order.required_technologies) != 0:
                print(f"\tOrder.required_technologies should be empty, found {len(test_order.required_technologies)} elements")
                points = 0.0

    print(f"Testing Order constructor finished: {points:.2f}/0.1 point")
    return points


def test_set_tasks():
    print("Testing Order.set_tasks()...")
    points = 0.0

    test_client = generate_name(10)
    test_offer = random.randint(100, 1000) * 10
    test_active = random.randint(1, 100)

    # test with correct inputs -> 0.1 point
    for _ in range(10):
        test_total_hours = random.randint(50, 200)
        test_dev_hours = random.randint(test_total_hours // 2, test_total_hours - 1)
        test_test_hours = test_total_hours - test_dev_hours
        try:
            test_order = st_ord.Order(test_client, test_offer, test_active, test_total_hours)
            test_order.set_tasks(test_dev_hours, test_test_hours)
        except Exception as e:
            print("Calling Order.set_tasks() cause an unexpected error:")
            print(e)
            break
        else:
            if 'development' not in test_order.stages:
                print(f"\tOrder.stages missing key 'development': {test_order.stages}")
                break
            if test_order.stages['development'] != test_dev_hours:
                print(f"\tDevelopment hours set incorrectly. Expected {test_dev_hours}, found {test_order.stages['development']}")
                break
            if 'testing' not in test_order.stages:
                print(f"\tOrder.stages missing key 'testing': {test_order.stages}")
                break
            if test_order.stages['testing'] != test_test_hours:
                print(f"\tTesting hours set incorrectly. Expected {test_test_hours}, found {test_order.stages['testing']}")
                break
    else:
        points += 0.1


    # test with incorrect inputs -> 0.1 point
    for _ in range(10):
        test_total_hours = random.randint(50, 200)
        test_dev_hours = random.randint(test_total_hours // 2, test_total_hours - 1)
        test_test_hours = test_total_hours - test_dev_hours + random.randint(-20, 20)
        while test_dev_hours + test_test_hours == test_total_hours:
            test_test_hours = test_total_hours - test_dev_hours + random.randint(-20, 20)

        try:
            test_order = st_ord.Order(test_client, test_offer, test_active, test_total_hours)
            test_order.set_tasks(test_dev_hours, test_test_hours)
        except ValueError:
            pass
        except Exception as e:
            print(f"Calling Order.set_tasks() with invalid values should cause a ValueError, got {type(e)}:")
            print(e)
            break
        else:
            print(f"Calling Order.set_tasks() with invalid values should cause a ValueError, no errors were generated:")
            break
    else:
        points += 0.1

    print(f"Testing Order.set_tasks() finished: {points:.2f}/0.2 points")
    return points


def test_add_required_technologies():
    print("Testing Order.add_required_technologies()...")
    points = 0.0

    # testing with one value - add one by one
    tests_passed = True
    should_have = []
    test_order = st_ord.Order("abc", 1000, 10, 25)
    for _ in range(3):
        new_tech = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        should_have.append(new_tech)
        try:
            test_order.add_required_technologies(new_tech)
        except Exception as e:
            print("\tCalling Order.add_required_technologies() cause an unexpected error:")
            print(e)
            tests_passed = False
            break
        else:
            for tech in should_have:
                try:
                    if tech not in test_order.required_technologies:
                        print(f"\tTechnology {tech} not found in list: {test_order.required_technologies}")
                        tests_passed = False
                        break
                except Exception as e:
                    print("\tCannot check presence of technology, wrong structure")
                    tests_passed = False
                    break
    if tests_passed:
        points += 0.1

    # testing with list - add all
    tests_passed = True
    should_have = []
    test_order = st_ord.Order("abc", 1000, 10, 25)
    for _ in range(3):
        test_list = []
        for t in range(random.randint(2, 4)):
            new_tech = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
            should_have.append(new_tech)
            test_list.append(new_tech)
        try:
            test_order.add_required_technologies(test_list)
        except Exception as e:
            print("\tCalling Order.add_required_technologies() cause an unexpected error:")
            print(e)
            tests_passed = False
            break
        else:
            for tech in should_have:
                try:
                    if tech not in test_order.required_technologies:
                        print(f"\tTechnology {tech} not found in list: {test_order.required_technologies}")
                        tests_passed = False
                        break
                except Exception as e:
                    print("\tCannot check presence of technology, wrong structure")
                    tests_passed = False
                    break
    if tests_passed:
        points += 0.1

    print(f"Testing Order.add_required_technologies() finished: {points:.2f}/0.2 points")
    return points


def main():
    print("Testing Order...")
    p1 = test_order_constructor()
    p2 = test_set_tasks()
    p3 = test_add_required_technologies()
    total = p1 + p2 + p3
    print(f"Testing Order finished: {total:.2f}/0.5 points")
    print()
    print(f"ORDER points: {total:.2f}/0.5 points")


if __name__ == '__main__':
    main()
