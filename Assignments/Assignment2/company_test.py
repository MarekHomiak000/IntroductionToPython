import company as st_comp
import employee as st_emp
import order as st_ord
import project as st_proj
import scheduler as st_sched


def test_calculate_total_income():
    print("Testing Company.calculate_total_income()...")
    points = 0.0

    # Company 1 - 1 Project
    dev1 = st_emp.Developer("Dev1", "junior", 20, ["Python"])
    test1 = st_emp.Tester("Test1", "junior", 20)
    man1 = st_emp.Manager("Man1", "junior", 20)
    order1 = st_ord.Order("ClientA", 10000, 1, 100)
    order1.set_tasks(60, 40)
    sched1 = st_sched.RandomScheduler([order1])
    company1 = st_comp.Company([dev1, test1, man1], sched1)
    project1 = st_proj.Project(company1, order1, 1, [dev1, test1, man1])
    company1.finished_projects.append(project1)
    try:
        st_res = company1.calculate_total_income()
    except Exception as e:
        print("\tCalling Company.get_total_income() cause an unexpected error")
        print(e)
    else:
        if st_res == 6400:
            points += 0.05
        else:
            print(f"\tCompany.get_total_income() returned wrong value. Expected 6400, got {st_res}")

    # Company 2 - 2 Projects
    dev2a = st_emp.Developer("Dev2a", "medior", 25, ["Python"])
    test2a = st_emp.Tester("Test2a", "medior", 25)
    man2a = st_emp.Manager("Man2a", "senior", 50)
    dev2b = st_emp.Developer("Dev2b", "junior", 20, ["Python"])
    test2b = st_emp.Tester("Test2b", "junior", 20)
    man2b = st_emp.Manager("Man2b", "junior", 20)

    order2a = st_ord.Order("ClientB1", 8000, 1, 80)
    order2a.set_tasks(50, 30)
    order2b = st_ord.Order("ClientB2", 7000, 1, 70)
    order2b.set_tasks(40, 30)

    sched2 = st_sched.RandomScheduler([order2a, order2b])
    company2 = st_comp.Company([dev2a, test2a, man2a, dev2b, test2b, man2b], sched2)

    project2a = st_proj.Project(company2, order2a, 1, [dev2a, test2a, man2a])

    project2b = st_proj.Project(company2, order2b, 2, [dev2b, test2b, man2b])

    company2.finished_projects.extend([project2a, project2b])
    try:
        st_res = company2.calculate_total_income()
    except Exception as e:
        print("\tCalling Company.get_total_income() cause an unexpected error")
        print(e)
    else:
        if st_res == 9280:
            points += 0.05
        else:
            print(f"\tCompany.get_total_income() returned wrong value. Expected 9280, got {st_res}")

    # Company 3 - 3 Projects
    devs3, tests3, mans3 = [], [], []
    employees3 = []
    sched3 = st_sched.RandomScheduler([])
    company3 = st_comp.Company(employees3, sched3)
    orders3 = [
        ("ClientC1", 9000, 60, 40),
        ("ClientC2", 8500, 50, 50),
        ("ClientC3", 8000, 55, 45),
    ]
    for idx, (client, price, dev_tasks, test_tasks) in enumerate(orders3, 1):
        dev = st_emp.Developer(f"Dev3_{idx}", "senior", 30, ["Java"])
        test = st_emp.Tester(f"Test3_{idx}", "senior", 30)
        man = st_emp.Manager(f"Man3_{idx}", "senior", 30)
        employees3.extend([dev, test, man])
        order = st_ord.Order(client, price, 1, dev_tasks + test_tasks)
        order.set_tasks(dev_tasks, test_tasks)
        project = st_proj.Project(company3, order, idx, [dev, test, man])
        company3.finished_projects.append(project)
    company3.employees = employees3
    try:
        st_res = company3.calculate_total_income()
    except Exception as e:
        print("\tCalling Company.get_total_income() cause an unexpected error")
        print(e)
    else:
        if st_res == 14700:
            points += 0.05
        else:
            print(f"\tCompany.get_total_income() returned wrong value. Expected 14700, got {st_res}")

    # Company 4 - 4 Projects
    employees4 = []
    sched4 = st_sched.RandomScheduler([])
    company4 = st_comp.Company(employees4, sched4)
    orders4 = [
        ("ClientD1", 10000, 60, 40),
        ("ClientD2", 9000, 55, 45),
        ("ClientD3", 9500, 50, 50),
        ("ClientD4", 11000, 65, 35)
    ]
    for idx, (client, price, dev_tasks, test_tasks) in enumerate(orders4, 1):
        dev = st_emp.Developer(f"Dev4_{idx}", "senior", 40, ["C++"])
        test = st_emp.Tester(f"Test4_{idx}", "senior", 40)
        man = st_emp.Manager(f"Man4_{idx}", "senior", 40)
        employees4.extend([dev, test, man])
        order = st_ord.Order(client, price, 1, dev_tasks + test_tasks)
        order.set_tasks(dev_tasks, test_tasks)
        project = st_proj.Project(company4, order, idx, [dev, test, man])
        company4.finished_projects.append(project)
    company4.employees = employees4
    try:
        st_res = company4.calculate_total_income()
    except Exception as e:
        print("\tCalling Company.get_total_income() cause an unexpected error")
        print(e)
    else:
        if st_res == 20300:
            points += 0.05
        else:
            print(f"\tCompany.get_total_income() returned wrong value. Expected 20300, got {st_res}")

    print(f"Testing Company.calculate_total_income() finished: {points:.2f}/0.2 points")
    return points



def test_get_available_employees():
    print("Testing Company.get_available_employees()...")
    points = 0.0

    # Scheduler setup
    scheduler1 = st_sched.RandomScheduler([])
    scheduler2 = st_sched.RandomScheduler([])

    # Company 1 setup
    dev1 = st_emp.Developer("Dev1", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Dev2", "medior", 25, ["Python"])
    test1 = st_emp.Tester("Test1", "junior", 20)
    man1 = st_emp.Manager("Man1", "junior", 20)
    company1 = st_comp.Company([dev1, dev2, test1, man1], scheduler1)

    # One project with all employees
    order1 = st_ord.Order("Client1", 10000, 1, 100)
    order1.set_tasks(60, 40)
    project1 = st_proj.Project(company1, order1, 1, [dev1, dev2, test1, man1])
    dev1.curr_project = project1
    dev2.curr_project = project1
    test1.curr_project = project1
    man1.curr_project = project1
    company1.active_projects.append(project1)

    # No employees should be available
    try:
        available1 = company1.get_available_employees(st_emp.Employee)
    except Exception as e:
        print("\tCalling Company.get_available_employees() cause an unexpected error:")
        print(e)
    else:
        if set(available1) == set():
            points += 0.05
        else:
            print(f"\tCompany.get_available_employees() returned wrong value. Expected empty list, got {available1}")

    # Company 2 setup
    dev3 = st_emp.Developer("Dev3", "senior", 30, ["Java"])
    test2 = st_emp.Tester("Test2", "senior", 30)
    man2 = st_emp.Manager("Man2", "senior", 30)
    test3 = st_emp.Tester("Test3", "medior", 25)
    dev4 = st_emp.Developer("Dev4", "junior", 20, ["C++"])
    company2 = st_comp.Company([dev3, test2, man2, test3, dev4], scheduler2)

    # One project with dev3 and test2 only
    order2 = st_ord.Order("Client2", 9000, 1, 80)
    order2.set_tasks(50, 30)
    project2 = st_proj.Project(company2, order2, 1, [man2, dev3, test2])
    dev3.curr_project = project2
    test2.curr_project = project2
    man2.curr_project = project2
    company2.active_projects.append(project2)

    # test3, and dev4 are available
    try:
        available2 = company2.get_available_employees(st_emp.Developer)
    except Exception as e:
        print("\tCalling Company.get_available_employees() cause an unexpected error:")
        print(e)
    else:
        if set(available2) == {dev4}:
            points += 0.025
        else:
            print(f"\tCompany.get_available_employees() returned wrong value. Expected {[dev4]} list, got {available2}")

    try:
        available2 = company2.get_available_employees(st_emp.Tester)
    except Exception as e:
        print("\tCalling Company.get_available_employees() cause an unexpected error:")
        print(e)
    else:
        if set(available2) == {test3}:
            points += 0.025
        else:
            print(f"\tCompany.get_available_employees() returned wrong value. Expected {[test3]} list, got {available2}")

    print(f"Testing Company.get_available_employees() finished: {points:.2f}/0.1 points")
    return points


def test_get_lang_developers():
    print("Testing Company.get_lang_developers()...")
    points = 0.0

    # Scheduler and company setup
    scheduler = st_sched.RandomScheduler([])
    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python", "Java"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java", "C++", "Go"])
    dev4 = st_emp.Developer("Dana", "junior", 20, ["Python"])
    tester = st_emp.Tester("Eve", "junior", 20)
    manager = st_emp.Manager("Frank", "junior", 20)

    company = st_comp.Company([dev1, dev2, dev3, dev4, tester, manager], scheduler)

    # Test 1: Python developers
    try:
        result = set(company.get_lang_developers("Python"))
        expected = {dev1, dev4}
        if result == expected:
            points += 0.025
        else:
            print(f"\tCalling Company.get_lang_developers() returned wrong value: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.get_lang_developers() caused an unexpected error:")
        print(e)

    # Test 2: Java developers
    try:
        result = set(company.get_lang_developers("Java"))
        expected = {dev1, dev3}
        if result == expected:
            points += 0.025
        else:
            print(f"\tCalling Company.get_lang_developers() returned wrong value: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.get_lang_developers() caused an unexpected error:")
        print(e)

    # Test 3: C++ developers
    try:
        result = set(company.get_lang_developers("C++"))
        expected = {dev2, dev3}
        if result == expected:
            points += 0.025
        else:
            print(f"\tCalling Company.get_lang_developers() returned wrong value: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.get_lang_developers() caused an unexpected error:")
        print(e)

    # Test 4: Go developers
    try:
        result = set(company.get_lang_developers("Go"))
        expected = {dev3}
        if result == expected:
            points += 0.025
        else:
            print(f"\tCalling Company.get_lang_developers() returned wrong value: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.get_lang_developers() caused an unexpected error:")
        print(e)

    print(f"Testing Company.get_lang_developers() finished: {points:.2f}/0.1 points")
    return points


def test_is_frequent_client():
    print("Testing Company.is_frequent_client()...")
    points = 0.0

    client1 = "ClientA"
    client2 = "ClientB"
    client3 = "ClientC"
    client4 = "ClientD"

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 20, ["Python"])
    tester = st_emp.Tester("Eve", "junior", 20)
    manager = st_emp.Manager("Frank", "junior", 20)

    order1 = st_ord.Order(client1, 1000, 1, 50)
    order2 = st_ord.Order(client2, 1500, 20, 75)
    order3 = st_ord.Order(client3, 1200, 30, 80)
    order4 = st_ord.Order(client1, 500, 40, 10)
    order5 = st_ord.Order(client4, 2000, 50, 75)
    order6 = st_ord.Order(client2, 1000, 60, 50)
    order7 = st_ord.Order(client1, 1000, 70, 50)
    order8 = st_ord.Order(client2, 1000, 80, 50)
    order9 = st_ord.Order(client2, 1000, 90, 50)
    order10 = st_ord.Order(client4, 1000, 100, 50)

    scheduler = st_sched.RandomScheduler(
        [order1, order2, order3, order4, order5,
         order6, order7, order8, order9, order10]
    )
    company = st_comp.Company([dev1, dev2, dev3, dev4, tester, manager], scheduler)

    # Simulate finished projects (Company has a finished_projects attribute)
    project1 = st_proj.Project(company, order1, 1, [manager, dev1, tester])
    project2 = st_proj.Project(company, order2, 20, [manager, dev2, tester])
    project3 = st_proj.Project(company, order3, 30, [manager, dev3, tester])
    project4 = st_proj.Project(company, order4, 40, [manager, dev4, tester])
    project5 = st_proj.Project(company, order5, 50, [manager, dev1, tester])
    project6 = st_proj.Project(company, order6, 60, [manager, dev2, tester])
    project7 = st_proj.Project(company, order7, 70, [manager, dev3, tester])
    project8 = st_proj.Project(company, order8, 80, [manager, dev4, tester])
    project9 = st_proj.Project(company, order9, 90, [manager, dev1, tester])
    project10 = st_proj.Project(company, order10, 100, [manager, dev2, tester])
    company.finished_projects = [
        project1, project2, project3, project4, project5,
        project6, project7, project8, project9, project10
    ]

    results = []

    try:
        result = company.is_frequent_client(client1)
        results.append(result)
        expected = True
        if result == expected:
            points += 0.05
        else:
            print(f"\tCompany.is_frequent_client() returned wrong value for ClientA: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.is_frequent_client() caused an unexpected error:")
        print(e)

    try:
        result = company.is_frequent_client(client2)
        results.append(result)
        expected = True
        if result == expected:
            points += 0.05
        else:
            print(f"\tCompany.is_frequent_client() returned wrong value for ClientB: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.is_frequent_client() caused an unexpected error:")
        print(e)

    try:
        result = company.is_frequent_client(client3)
        results.append(result)
        expected = False
        if result == expected:
            points += 0.05
        else:
            print(f"\tCompany.is_frequent_client() returned wrong value for ClientC: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.is_frequent_client() caused an unexpected error:")
        print(e)

    try:
        result = company.is_frequent_client(client4)
        results.append(result)
        expected = False
        if result == expected:
            points += 0.05
        else:
            print(f"\tCompany.is_frequent_client() returned wrong value for ClientD: expected {expected}, got {result}")
    except Exception as e:
        print("\tCalling Company.is_frequent_client() caused an unexpected error:")
        print(e)

    # if always True or False
    if sum(results) == 0 or sum(results) == 4:
        points = 0.0

    print(f"Testing Company.is_frequent_client() finished: {points:.2f}/0.2 points")
    return points


def test_close_project():
    print("Testing Company.close_project()...")
    points = 0.0

    client1 = "ClientA"
    client2 = "ClientB"
    client3 = "ClientC"

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 20, ["Python"])
    tester = st_emp.Tester("Eve", "junior", 20)
    manager1 = st_emp.Manager("Frank", "junior", 20)
    manager2 = st_emp.Manager("Fred", "junior", 20)

    order1 = st_ord.Order(client1, 1000, 1, 50)
    order2 = st_ord.Order(client2, 1500, 20, 75)
    order3 = st_ord.Order(client3, 1200, 30, 80)
    order4 = st_ord.Order(client1, 500, 31, 10)

    scheduler = st_sched.RandomScheduler(
        [order1, order2, order3, order4]
    )
    company = st_comp.Company([dev1, dev2, dev3, dev4, tester, manager1, manager2], scheduler)

    # Simulate finished projects (Company has a finished_projects attribute)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester])
    project2 = st_proj.Project(company, order2, 20, [manager1, dev2, tester])
    project3 = st_proj.Project(company, order3, 30, [manager1, dev3, tester])
    project4 = st_proj.Project(company, order4, 31, [manager2, dev4])
    company.active_projects = [project3, project4]

    try:
        company.close_project(project1)
    except Exception as e:
        print("\tCompany.close_project() shouldn't cause an error for inactive projects")
        print(e)
    else:
        points += 0.1

    try:
        company.close_project(project3)
    except Exception as e:
        print("\tCalling Company.close_project() caused an unexpected error:")
        print(e)
    else:
        if project3 in company.active_projects:
            print("\tCalling Company.close_project did not move project from active_projects")
        else:
            points += 0.05
        if project3 not in company.finished_projects:
            print("\tCalling Company.close_project did not move project to finished_projects")
        else:
            points += 0.05

    print(f"Testing Company.close_project() finished: {points:.2f}/0.2 points")
    return points


def test_solving():
    print("Testing Company.solving()...")
    points = 0.0

    client1 = "ClientA"
    client2 = "ClientB"
    client3 = "ClientC"

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 20, ["Python"])
    tester = st_emp.Tester("Eve", "junior", 20)
    manager1 = st_emp.Manager("Frank", "junior", 20)
    manager2 = st_emp.Manager("Fred", "junior", 20)

    order1 = st_ord.Order(client1, 1000, 1, 50)
    order2 = st_ord.Order(client2, 1500, 20, 75)
    order3 = st_ord.Order(client3, 1200, 30, 80)
    order4 = st_ord.Order(client1, 500, 31, 10)

    scheduler = st_sched.RandomScheduler(
        [order1, order2, order3, order4]
    )
    company = st_comp.Company([dev1, dev2, dev3, dev4, tester, manager1, manager2], scheduler)

    # Simulate finished projects (Company has a finished_projects attribute)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester])
    project2 = st_proj.Project(company, order2, 20, [manager1, dev2, tester])
    project3 = st_proj.Project(company, order3, 30, [manager1, dev3, tester])
    project4 = st_proj.Project(company, order4, 31, [manager2, dev4])
    company.finished_projects = [project1]
    company.active_projects = [project3, project4]

    try:
        st_res = company.solving(order1)
    except Exception as e:
        print("\tCalling Company.solving() caused an unexpected error:")
        print(e)
    else:
        if st_res != True:
            print(f"\tCompany.solving() returned wrong value. Expected True, got {st_res}")
        else:
            points += 0.05

    try:
        st_res = company.solving(order2)
    except Exception as e:
        print("\tCalling Company.solving() caused an unexpected error:")
        print(e)
    else:
        if st_res != False:
            print(f"\tCompany.solving() returned wrong value. Expected False, got {st_res}")
        else:
            points += 0.05
    try:
        st_res = company.solving(order3)
    except Exception as e:
        print("\tCalling Company.solving() caused an unexpected error:")
        print(e)
    else:
        if st_res != True:
            print(f"\tCompany.solving() returned wrong value. Expected True, got {st_res}")
        else:
            points += 0.05

    try:
        st_res = company.solving(order4)
    except Exception as e:
        print("\tCalling Company.solving() caused an unexpected error:")
        print(e)
    else:
        if st_res != True:
            print(f"\tCompany.solving() returned wrong value. Expected True, got {st_res}")
        else:
            points += 0.05

    print(f"Testing Company.solving() finished: {points:.2f}/0.2 points")
    return points


def test_can_solve_order():
    print("Testing Company.can_solve_order()...")
    points = 0.0

    dev1 = st_emp.Developer("Dev1", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Dev2", "medior", 25, ["Python", "html"])
    test1 = st_emp.Tester("Test1", "junior", 20)
    man1 = st_emp.Manager("Man1", "junior", 20)
    order1 = st_ord.Order("Client1", 10000, 1, 100)
    order1.set_tasks(60, 40)
    scheduler1 = st_sched.RandomScheduler([order1])
    company1 = st_comp.Company([dev1, dev2, test1, man1], scheduler1)
    company1.employees = [dev1, dev2, test1, man1]

    # One project with all employees
    project1 = st_proj.Project(company1, order1, 1, [dev1, test1, man1])
    dev1.curr_project = project1
    test1.curr_project = project1
    man1.curr_project = project1
    company1.active_projects.append(project1)
    results = []

    # test case 1: no manager available
    try:
        test_order = st_ord.Order("Client2", 10000, 2, 200)
        test_order.stages = {'development': 180, 'testing': 20}
        test_order.required_technologies = ["Python", "html"]
        st_res = company1.can_solve_order(test_order)
        results.append(st_res)
    except Exception as e:
        print("\tCalling Company.can_solve_order() caused an unexpected error:")
        print(e)
    else:
        if st_res != False:
            print(f"\tCompany.can_solve_order() returned wrong value. Expected False, got {st_res}")
        else:
            points += 0.1

    man2 = st_emp.Manager("Man2", "junior", 20)
    company1.employees = [dev1, dev2, test1, man1, man2]
    # test case 2: no developer available for C++
    try:
        test_order = st_ord.Order("Client2", 10000, 2, 200)
        test_order.stages = {'development': 180, 'testing': 20}
        test_order.required_technologies = ["Python", "C++"]
        st_res = company1.can_solve_order(test_order)
        results.append(st_res)
    except Exception as e:
        print("\tCalling Company.can_solve_order() caused an unexpected error:")
        print(e)
    else:
        if st_res != False:
            print(f"\tCompany.can_solve_order() returned wrong value. Expected False, got {st_res}")
        else:
            points += 0.1

    # test case 3: only one developer available for both languages
    try:
        test_order = st_ord.Order("Client2", 10000, 2, 200)
        test_order.stages = {'development': 180, 'testing': 20}
        test_order.required_technologies = ["Python", "html"]
        st_res = company1.can_solve_order(test_order)
        results.append(st_res)
    except Exception as e:
        print("\tCalling Company.can_solve_order() caused an unexpected error:")
        print(e)
    else:
        if st_res != False:
            print(f"\tCompany.can_solve_order() returned wrong value. Expected False, got {st_res}")
        else:
            points += 0.1

    # test case 4: no tester is available
    try:
        test_order = st_ord.Order("Client2", 10000, 2, 200)
        test_order.stages = {'development': 180, 'testing': 20}
        test_order.required_technologies = ["Python"]
        st_res = company1.can_solve_order(test_order)
        results.append(st_res)
    except Exception as e:
        print("\tCalling Company.can_solve_order() caused an unexpected error:")
        print(e)
    else:
        if st_res != False:
            print(f"\tCompany.can_solve_order() returned wrong value. Expected False, got {st_res}")
        else:
            points += 0.1

    test2 = st_emp.Tester("Test2", "junior", 20)
    company1.employees = [dev1, dev2, test1, test2, man1, man2]
    # test case 5: everything in order
    try:
        test_order = st_ord.Order("Client2", 10000, 2, 200)
        test_order.stages = {'development': 180, 'testing': 20}
        test_order.required_technologies = ["Python"]
        st_res = company1.can_solve_order(test_order)
        results.append(st_res)
    except Exception as e:
        print("\tCalling Company.can_solve_order() caused an unexpected error:")
        print(e)
    else:
        if st_res != True:
            print(f"\tCompany.can_solve_order() returned wrong value. Expected True, got {st_res}")
        else:
            points += 0.1

    # if always True or False
    if sum(results) == 0 or sum(results) == 4:
        points = 0.0

    print(f"Testing Company.can_solve_order() finished: {points:.2f}/0.5 points")
    return points


def test_simulate_day():
    print("Testing Company.simulate_day()...")
    points = 0.0

    added_new_projects = False
    updated_remaining_hours = True
    removed_finished_projects = False

    client1 = "ClientA"
    client2 = "ClientB"
    client3 = "ClientC"

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 20, ["Python"])
    tester1 = st_emp.Tester("Eve", "junior", 20)
    tester2 = st_emp.Tester("Eve", "junior", 20)
    tester3 = st_emp.Tester("Eve", "junior", 20)
    manager1 = st_emp.Manager("Frank", "junior", 20)
    manager2 = st_emp.Manager("Fred", "junior", 20)

    order1 = st_ord.Order(client1, 1000, 1, 50)
    order1.stages = {'development': 40, 'testing': 10}
    order1.required_technologies = ["Python"]
    order2 = st_ord.Order(client2, 1500, 2, 75)
    order2.stages = {'development': 60, 'testing': 15}
    order2.required_technologies = ["C++"]
    order3 = st_ord.Order(client3, 1200, 3, 80)
    order3.stages = {'development': 60, 'testing': 20}
    order3.required_technologies = ["Java"]
    order4 = st_ord.Order(client1, 500, 4, 10)
    order4.stages = {'development': 6, 'testing': 4}
    order4.required_technologies = ["Python"]

    scheduler = st_sched.RandomScheduler(
        [order1, order2, order3, order4]
    )
    company = st_comp.Company([dev1, dev2, dev3, dev4, tester1, tester2, tester3, manager1, manager2], scheduler)
    company.employees = [dev1, dev2, dev3, dev4, tester1, tester2, tester3, manager1, manager2]

    company.active_projects = []
    company.finished_projects = []

    active_lengths = [0]
    finished_lengths = [0]
    project_hours = {}
    for day in range(1, 201):
        try:
            company.simulate_day(day)
        except Exception as e:
            print("Calling Company.simulate_day() caused an unexpected error:")
            print(e)
        else:
            for project in company.active_projects:
                if project not in project_hours:
                    project_hours[project] = [project.remaining_hours]
                else:
                    project_hours[project].append(project.remaining_hours)
            active_lengths.append(len(company.active_projects))
            finished_lengths.append(len(company.finished_projects))

    for idx in range(1, len(active_lengths)):
        if active_lengths[idx] > active_lengths[idx - 1]:
            added_new_projects = True
    if any(finished_lengths):
        removed_finished_projects = True

    for project in project_hours:
        if len(project_hours[project]) == 1:
            continue
        for idx in range(1, len(project_hours[project])):
            if project_hours[project][idx] >= project_hours[project][idx - 1]:
                updated_remaining_hours = False

    if added_new_projects:
        points += 0.2
    if removed_finished_projects:
        points += 0.2
    if updated_remaining_hours:
        points += 0.1

    print(f"Testing Company.simulate_day() finished: {points:.2f}/0.5 points")
    return points


def main():
    print("Testing Company...")
    p1 = test_calculate_total_income()
    p2 = test_get_available_employees()
    p3 = test_get_lang_developers()
    p4 = test_is_frequent_client()
    p5 = test_close_project()
    p6 = test_solving()
    p7 = test_can_solve_order()
    p8 = test_simulate_day()
    total = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8
    print(f"Testing Company finished: {total:.2f}/2 points")
    print()
    print(f"COMPANY points: {total:.2f}/2 points")


if __name__ == '__main__':
    main()
