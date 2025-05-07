import company as st_comp
import employee as st_emp
import order as st_ord
import project as st_proj
import scheduler as st_sched


def test_set_company():
    print("Testing Scheduler.set_company()...")
    points = 0.0

    test_scheduler = st_sched.Scheduler([])
    test_company = st_comp.Company([], test_scheduler)
    test_scheduler.company = None

    try:
        test_scheduler.set_company(test_company)
    except Exception as e:
        print("\tCalling Scheduler.set_company() caused an unexpected error:")
        print(e)
    else:
        if test_scheduler.company == test_company:
            points += 0.1
        else:
            print("\tCalling Scheduler.set_company() did not update Scheduler.company variable")

    print(f"Testing Scheduler.set_company() finished: {points:.2f}/0.1 point")
    return points


def test_get_active_offers():
    print("Testing Scheduler.get_active_offers()...")
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
    order2 = st_ord.Order(client2, 1500, 2, 75)
    order3 = st_ord.Order(client3, 1200, 3, 80)
    order4 = st_ord.Order(client1, 500, 5, 10)
    order5 = st_ord.Order(client1, 500, 10, 10)

    test_scheduler = st_sched.Scheduler([order1, order2, order3, order4, order5])
    company = st_comp.Company([dev1, dev2, dev3, dev4, tester, manager1, manager2], test_scheduler)

    # Simulate finished projects (Company has a finished_projects attribute)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester])
    company.active_projects = [project1]

    correct = [
        [],
        [],
        [order2],
        [order2, order3],
        [order2, order3],
        [order3, order4],
        [order4],
        [order4],
        [],
        [],
        [order5]
    ]

    for day in range(1, 11):
        try:
            st_res = test_scheduler.get_active_offers(day)
        except Exception as e:
            print("\tCalling Scheduler.get_active_offers() caused an unexpected exception:")
            print(e)
        else:
            if set(st_res) != set(correct[day]):
                print(f"\tScheduler.get_active_offers() returned wrong value. Expected {set(correct[day])}, got {st_res}")
            else:
                points += 0.02

    print(f"Testing Scheduler.get_active_offers() finished: {points:.2f}/0.2 points")
    return points


def test_get_new_project():
    print("Testing Scheduler.get_new_project()...")
    points = 0.0

    for sched_type in [st_sched.FirstScheduler, st_sched.RandomScheduler, st_sched.GreedyScheduler, st_sched.CheapestEmployeeScheduler]:
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
        order2 = st_ord.Order(client2, 1500, 2, 75)
        order3 = st_ord.Order(client3, 1200, 3, 80)
        order4 = st_ord.Order(client1, 500, 5, 10)
        order5 = st_ord.Order(client1, 500, 10, 10)

        test_scheduler = sched_type([order1, order2, order3, order4, order5])

        # company not yet set
        company_pass = False
        try:
            st_res = test_scheduler.get_new_project(3)
        except Exception as e:
            print("\tCalling Scheduler.get_new_project() caused an unexpected error:")
            print(e)
        else:
            if st_res != None:
                print(f"\tScheduler.get_new_project() should return None if company was not set, got {st_res}")
            else:
                company_pass = True

        company = st_comp.Company([dev1, dev2, dev3, dev4, tester, manager1, manager2], test_scheduler)
        test_scheduler.company = company

        try:
            st_res = test_scheduler.get_new_project(3)
        except Exception as e:
            print("\tCalling Scheduler.get_new_project() caused an unexpected error:")
            print(e)
        else:
            if not isinstance(st_res, st_proj.Project):
                print(f"\tScheduler.get_new_project() returned wrong type. Expected Project, got {type(st_res)}")
            else:
                points += 0.1
                if company_pass:
                    points += 0.1
                break

    print(f"Testing Scheduler.get_new_project() finished: {points:.2f}/0.2 points")
    return points


def get_manager(emp_list):
    managers = [emp for emp in emp_list if isinstance(emp, st_emp.Manager)]
    if len(managers) != 1:
        return None
    return managers[0]


def validate_employees(emp_list, technologies):
    managers = [emp for emp in emp_list if isinstance(emp, st_emp.Manager)]
    if len(managers) != 1:
        return False

    testers = [emp for emp in emp_list if isinstance(emp, st_emp.Tester)]
    if len(testers) == 0:
        return False

    devs = [emp for emp in emp_list if isinstance(emp, st_emp.Developer)]
    if len(devs) == 0:
        return False

    for technology in technologies:
        for dev in devs:
            if technology in dev.languages:
                break
        else:
            return False

    return True


def test_FirstScheduler():
    print("Testing FirstScheduler...")
    points = 0.0

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 17, ["C#"])
    dev5 = st_emp.Developer("Sue", "medior", 27, ["Python"])
    dev6 = st_emp.Developer("Stephen", "senior", 32, ["Python"])
    dev7 = st_emp.Developer("Alan", "junior", 23, ["Python"])
    dev8 = st_emp.Developer("Jill", "medior", 22, ["Java"])
    dev9 = st_emp.Developer("Joe", "senior", 38, ["Python"])
    dev10 = st_emp.Developer("Rick", "junior", 20, ["Python"])

    tester1 = st_emp.Tester("Eve", "junior", 20)
    tester2 = st_emp.Tester("John", "junior", 20)
    tester3 = st_emp.Tester("Jack", "junior", 20)
    manager1 = st_emp.Manager("Frank", "senior", 35)
    manager2 = st_emp.Manager("Fred", "junior", 20)
    manager3 = st_emp.Manager("David", "medior", 27)

    all_emps = [
        dev1, dev2, dev3, dev4, dev5, dev6, dev7,
        dev8, dev9, dev10, tester1, tester2, tester3,
        manager1, manager2, manager3
    ]

    order1 = st_ord.Order("ClientA", 1000, 1, 200)
    order1.stages = {'development': 180, 'testing': 20}
    order1.required_technologies = ["Python"]
    order2 = st_ord.Order("ClientB", 1500, 2, 75)
    order2.stages = {'development': 60, 'testing': 15}
    order2.required_technologies = ["Python", "html"]
    order3 = st_ord.Order("ClientC", 1200, 3, 80)
    order3.stages = {'development': 60, 'testing': 20}
    order3.required_technologies = ["Assembly"]
    order4 = st_ord.Order("ClientD", 1200, 3, 20)
    order4.stages = {'development': 8, 'testing': 2}
    order4.required_technologies = ["C++", "Python"]
    order5 = st_ord.Order("ClientE", 2400, 4, 100)
    order5.stages = {'development': 90, 'testing': 10}
    order5.required_technologies = ["Java", "C#"]
    order6 = st_ord.Order("ClientF", 5700, 4, 250)
    order6.stages = {'development': 200, 'testing': 50}
    order6.required_technologies = ["Python"]
    order7 = st_ord.Order("ClientG", 3600, 5, 200)
    order7.stages = {'development': 160, 'testing': 40}
    order7.required_technologies = ["Python"]
    order8 = st_ord.Order("ClientH", 14000, 5, 300)
    order8.stages = {'development': 260, 'testing': 40}
    order8.required_technologies = ["html"]
    order9 = st_ord.Order("ClientI", 2400, 7, 80)
    order9.stages = {'development': 70, 'testing': 10}
    order9.required_technologies = ["Java"]
    order10 = st_ord.Order("ClientJ", 5000, 8, 150)
    order10.stages = {'development': 130, 'testing': 20}
    order10.required_technologies = ["C++"]

    test_scheduler = st_sched.FirstScheduler([
        order1, order2, order3, order4, order5,
        order6, order7, order8, order9, order10
    ])
    company = st_comp.Company(all_emps, test_scheduler)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester1])

    company.active_projects = [project1]
    corr_client = "ClientD"

    selects_correct = True
    right_manager = True
    changes_emps = False
    valid_project = True

    emp_selection = None
    has_result = False

    for _ in range(20):
        try:
            st_off, st_emps = test_scheduler.select_offer([order3, order4, order5, order6, order7, order8])
        except Exception as e:
            print("\tCalling FirstScheduler.select_offer() caused an unexpected exception")
            print(e)
        else:
            if not isinstance(st_off, st_ord.Order):
                print(f"\tFirstScheduler.select_offer() should return Order object, got {type(st_off)}")
            else:
                has_result = True
                if st_off.client != corr_client:
                    selects_correct = False
                    print(f"\tFirstScheduler.select_offer() selected incorrect offer")

                if get_manager(st_emps) != manager2:
                    right_manager = False
                    print(f"\tFirstScheduler.select_offer() selected incorrect manager")

                if emp_selection is None:
                    emp_selection = st_emps.copy()
                else:
                    if set(emp_selection) != set(st_emps):
                        changes_emps = True

                if not validate_employees(st_emps, order4.required_technologies):
                    valid_project = False
                    print(f"\tFirstScheduler.select_offer() selected wrong employees")

    if selects_correct:
        points += 0.2
    if right_manager:
        points += 0.1
    if changes_emps:
        points += 0.1
    else:
        print("\tFirstScheduler should select employees randomly")
    if valid_project:
        points += 0.1

    if not has_result:
        points = 0.0

    print(f"Testing FirstScheduler finished: {points:.2f}/0.5 points")
    return points


def test_RandomScheduler():
    print("Testing RandomScheduler...")
    points = 0.0

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 17, ["C#"])
    dev5 = st_emp.Developer("Sue", "medior", 27, ["Python"])
    dev6 = st_emp.Developer("Stephen", "senior", 32, ["Python"])
    dev7 = st_emp.Developer("Alan", "junior", 23, ["Python"])
    dev8 = st_emp.Developer("Jill", "medior", 22, ["Java"])
    dev9 = st_emp.Developer("Joe", "senior", 38, ["Python"])
    dev10 = st_emp.Developer("Rick", "junior", 20, ["Python"])

    tester1 = st_emp.Tester("Eve", "junior", 20)
    tester2 = st_emp.Tester("John", "junior", 20)
    tester3 = st_emp.Tester("Jack", "junior", 20)
    manager1 = st_emp.Manager("Frank", "senior", 35)
    manager2 = st_emp.Manager("Fred", "junior", 20)
    manager3 = st_emp.Manager("David", "medior", 27)

    all_emps = [
        dev1, dev2, dev3, dev4, dev5, dev6, dev7,
        dev8, dev9, dev10, tester1, tester2, tester3,
        manager1, manager2, manager3
    ]

    order1 = st_ord.Order("ClientA", 1000, 1, 200)
    order1.stages = {'development': 180, 'testing': 20}
    order1.required_technologies = ["Python"]
    order2 = st_ord.Order("ClientB", 1500, 2, 75)
    order2.stages = {'development': 60, 'testing': 15}
    order2.required_technologies = ["Python", "html"]
    order3 = st_ord.Order("ClientC", 1200, 3, 80)
    order3.stages = {'development': 60, 'testing': 20}
    order3.required_technologies = ["Assembly"]
    order4 = st_ord.Order("ClientD", 1200, 3, 20)
    order4.stages = {'development': 8, 'testing': 2}
    order4.required_technologies = ["C++", "Python"]
    order5 = st_ord.Order("ClientE", 2400, 4, 100)
    order5.stages = {'development': 90, 'testing': 10}
    order5.required_technologies = ["Java", "C#"]
    order6 = st_ord.Order("ClientF", 5700, 4, 250)
    order6.stages = {'development': 200, 'testing': 50}
    order6.required_technologies = ["Python"]
    order7 = st_ord.Order("ClientG", 3600, 5, 200)
    order7.stages = {'development': 160, 'testing': 40}
    order7.required_technologies = ["Python"]
    order8 = st_ord.Order("ClientH", 14000, 5, 300)
    order8.stages = {'development': 260, 'testing': 40}
    order8.required_technologies = ["html"]
    order9 = st_ord.Order("ClientI", 2400, 7, 80)
    order9.stages = {'development': 70, 'testing': 10}
    order9.required_technologies = ["Java"]
    order10 = st_ord.Order("ClientJ", 5000, 8, 150)
    order10.stages = {'development': 130, 'testing': 20}
    order10.required_technologies = ["C++"]

    test_scheduler = st_sched.RandomScheduler([
        order1, order2, order3, order4, order5,
        order6, order7, order8, order9, order10
    ])
    company = st_comp.Company(all_emps, test_scheduler)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester1])

    company.active_projects = [project1]

    correct_clients = ["ClientD", "ClientE", "ClientF", "ClientG"]
    selects_correct = True
    changes_emps = False
    valid_project = True

    emp_selection = None
    has_result = False

    selected_managers = []
    for _ in range(20):
        try:
            st_off, st_emps = test_scheduler.select_offer([order3, order4, order5, order6, order7, order8])
        except Exception as e:
            print("\tCalling RandomScheduler.select_offer() caused an unexpected exception")
            print(e)
        else:
            if not isinstance(st_off, st_ord.Order):
                print(f"\tRandomScheduler.select_offer() should return Order object, got {type(st_off)}")
            else:
                has_result = True
                if st_off.client not in correct_clients:
                    selects_correct = False
                    print(f"\tRandomScheduler.select_offer() selected incorrect offer")

                selected_managers.append(get_manager(st_emps))

                if emp_selection is None:
                    emp_selection = st_emps.copy()
                else:
                    if set(emp_selection) != set(st_emps):
                        changes_emps = True

                if not validate_employees(st_emps, st_off.required_technologies):
                    valid_project = False
                    print(f"\tRandomScheduler.select_offer() selected wrong employees")

    if selects_correct:
        points += 0.2
    if len(set(selected_managers)) > 1:
        points += 0.1
    if changes_emps:
        points += 0.1
    else:
        print("\tRandomScheduler should select employees randomly")
    if valid_project:
        points += 0.1

    if not has_result:
        points = 0.0

    print(f"Testing RandomScheduler finished: {points:.2f}/0.5 points")
    return points


def test_GreedyScheduler():
    print("Testing GreedyScheduler...")
    points = 0.0

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 17, ["C#"])
    dev5 = st_emp.Developer("Sue", "medior", 27, ["Python"])
    dev6 = st_emp.Developer("Stephen", "senior", 32, ["Python"])
    dev7 = st_emp.Developer("Alan", "junior", 23, ["Python"])
    dev8 = st_emp.Developer("Jill", "medior", 22, ["Java"])
    dev9 = st_emp.Developer("Joe", "senior", 38, ["Python"])
    dev10 = st_emp.Developer("Rick", "junior", 20, ["Python"])

    tester1 = st_emp.Tester("Eve", "junior", 20)
    tester2 = st_emp.Tester("John", "junior", 20)
    tester3 = st_emp.Tester("Jack", "junior", 20)
    manager1 = st_emp.Manager("Frank", "senior", 35)
    manager2 = st_emp.Manager("Fred", "junior", 20)
    manager3 = st_emp.Manager("David", "medior", 27)

    all_emps = [
        dev1, dev2, dev3, dev4, dev5, dev6, dev7,
        dev8, dev9, dev10, tester1, tester2, tester3,
        manager1, manager2, manager3
    ]

    order1 = st_ord.Order("ClientA", 1000, 1, 200)
    order1.stages = {'development': 180, 'testing': 20}
    order1.required_technologies = ["Python"]
    order2 = st_ord.Order("ClientB", 1500, 2, 75)
    order2.stages = {'development': 60, 'testing': 15}
    order2.required_technologies = ["Python", "html"]
    order3 = st_ord.Order("ClientC", 1200, 3, 80)
    order3.stages = {'development': 60, 'testing': 20}
    order3.required_technologies = ["Assembly"]
    order4 = st_ord.Order("ClientD", 1200, 3, 20)
    order4.stages = {'development': 8, 'testing': 2}
    order4.required_technologies = ["C++", "Python"]
    order5 = st_ord.Order("ClientE", 2400, 4, 100)
    order5.stages = {'development': 90, 'testing': 10}
    order5.required_technologies = ["Java", "C#"]
    order6 = st_ord.Order("ClientF", 5700, 4, 250)
    order6.stages = {'development': 200, 'testing': 50}
    order6.required_technologies = ["Python"]
    order7 = st_ord.Order("ClientG", 3600, 5, 200)
    order7.stages = {'development': 160, 'testing': 40}
    order7.required_technologies = ["Python"]
    order8 = st_ord.Order("ClientH", 14000, 5, 300)
    order8.stages = {'development': 260, 'testing': 40}
    order8.required_technologies = ["html"]
    order9 = st_ord.Order("ClientI", 2400, 7, 80)
    order9.stages = {'development': 70, 'testing': 10}
    order9.required_technologies = ["Java"]
    order10 = st_ord.Order("ClientJ", 5000, 8, 150)
    order10.stages = {'development': 130, 'testing': 20}
    order10.required_technologies = ["C++"]

    test_scheduler = st_sched.GreedyScheduler([
        order1, order2, order3, order4, order5,
        order6, order7, order8, order9, order10
    ])
    company = st_comp.Company(all_emps, test_scheduler)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester1])

    company.active_projects = [project1]
    corr_client = "ClientF"

    selects_correct = True
    changes_emps = False
    valid_project = True

    emp_selection = None
    has_result = False

    selected_managers = []
    for _ in range(20):
        try:
            st_off, st_emps = test_scheduler.select_offer([order3, order4, order5, order6, order7, order8])
        except Exception as e:
            print("\tCalling GreedyScheduler.select_offer() caused an unexpected exception")
            print(e)
        else:
            if not isinstance(st_off, st_ord.Order):
                print(f"\tGreedyScheduler.select_offer() should return Order object, got {type(st_off)}")
            else:
                has_result = True
                if st_off.client != corr_client:
                    selects_correct = False
                    print(f"\tGreedyScheduler.select_offer() selected incorrect offer")

                selected_managers.append(get_manager(st_emps))

                if emp_selection is None:
                    emp_selection = st_emps.copy()
                else:
                    if set(emp_selection) != set(st_emps):
                        changes_emps = True

                if not validate_employees(st_emps, order6.required_technologies):
                    valid_project = False
                    print(f"\tGreedyScheduler.select_offer() selected wrong employees")

    if selects_correct:
        points += 0.4
    if len(set(selected_managers)) > 1:
        points += 0.2
    if changes_emps:
        points += 0.2
    else:
        print("\tGreedyScheduler should select employees randomly")
    if valid_project:
        points += 0.2

    if not has_result:
        points = 0.0

    print(f"Testing GreedyScheduler finished: {points:.2f}/1 point")
    return points


def test_CheapestEmployeeScheduler():
    print("Testing CheapestEmployeeScheduler...")
    points = 0.0

    dev1 = st_emp.Developer("Alice", "junior", 20, ["Python"])
    dev2 = st_emp.Developer("Bob", "medior", 25, ["C++"])
    dev3 = st_emp.Developer("Charlie", "senior", 30, ["Java"])
    dev4 = st_emp.Developer("Dana", "junior", 17, ["C#"])
    dev5 = st_emp.Developer("Sue", "medior", 27, ["Python"])
    dev6 = st_emp.Developer("Stephen", "senior", 32, ["Python"])
    dev7 = st_emp.Developer("Alan", "junior", 23, ["Python"])
    dev8 = st_emp.Developer("Jill", "medior", 22, ["Java"])
    dev9 = st_emp.Developer("Joe", "senior", 38, ["Python"])
    dev10 = st_emp.Developer("Rick", "junior", 20, ["Python"])

    tester1 = st_emp.Tester("Eve", "junior", 20)
    tester2 = st_emp.Tester("John", "junior", 20)
    tester3 = st_emp.Tester("Jack", "senior", 35)
    manager1 = st_emp.Manager("Frank", "senior", 35)
    manager2 = st_emp.Manager("Fred", "junior", 20)
    manager3 = st_emp.Manager("David", "medior", 27)

    all_emps = [
        dev1, dev2, dev3, dev4, dev5, dev6, dev7,
        dev8, dev9, dev10, tester1, tester2, tester3,
        manager1, manager2, manager3
    ]

    order1 = st_ord.Order("ClientA", 1000, 1, 200)
    order1.stages = {'development': 180, 'testing': 20}
    order1.required_technologies = ["Python"]
    order2 = st_ord.Order("ClientB", 1500, 2, 75)
    order2.stages = {'development': 60, 'testing': 15}
    order2.required_technologies = ["Python", "html"]
    order3 = st_ord.Order("ClientC", 1200, 3, 80)
    order3.stages = {'development': 60, 'testing': 20}
    order3.required_technologies = ["Assembly"]
    order4 = st_ord.Order("ClientD", 1200, 3, 20)
    order4.stages = {'development': 8, 'testing': 2}
    order4.required_technologies = ["C++", "Python"]
    order5 = st_ord.Order("ClientE", 2400, 4, 100)
    order5.stages = {'development': 90, 'testing': 10}
    order5.required_technologies = ["Java", "C#"]
    order6 = st_ord.Order("ClientF", 5700, 4, 10)
    order6.stages = {'development': 7, 'testing': 3}
    order6.required_technologies = ["Python"]
    order7 = st_ord.Order("ClientG", 3600, 5, 200)
    order7.stages = {'development': 160, 'testing': 40}
    order7.required_technologies = ["Python"]
    order8 = st_ord.Order("ClientH", 14000, 5, 300)
    order8.stages = {'development': 260, 'testing': 40}
    order8.required_technologies = ["html"]
    order9 = st_ord.Order("ClientI", 2400, 7, 80)
    order9.stages = {'development': 70, 'testing': 10}
    order9.required_technologies = ["Java"]
    order10 = st_ord.Order("ClientJ", 5000, 8, 150)
    order10.stages = {'development': 130, 'testing': 20}
    order10.required_technologies = ["C++"]

    test_scheduler = st_sched.CheapestEmployeeScheduler([
        order1, order2, order3, order4, order5,
        order6, order7, order8, order9, order10
    ])
    company = st_comp.Company(all_emps, test_scheduler)
    project1 = st_proj.Project(company, order1, 1, [manager1, dev1, tester1])

    company.active_projects = [project1]
    corr_client = "ClientF"
    corr_manager = manager2
    corr_dev = dev10
    corr_tester = tester2
    corr_emps = set([corr_manager, corr_dev, corr_tester])

    selects_correct = True
    correct_emps = True
    valid_project = True
    has_result = False

    for _ in range(20):
        try:
            st_off, st_emps = test_scheduler.select_offer([order3, order4, order5, order6, order7, order8])
        except Exception as e:
            print("\tCalling CheapestEmployeeScheduler.select_offer() caused an unexpected exception")
            print(e)
        else:
            if not isinstance(st_off, st_ord.Order):
                print(f"\tCheapestEmployeeScheduler.select_offer() should return Order object, got {type(st_off)}")
            else:
                has_result = True
                if st_off.client != corr_client:
                    selects_correct = False
                    print(f"\tCheapestEmployeeScheduler.select_offer() selected incorrect offer")

                if set(st_emps) != corr_emps:
                    correct_emps = False
                    print(f"\tCheapestEmployeeScheduler.select_offer() did not select cheapest available employees")

                if not validate_employees(st_emps, order6.required_technologies):
                    valid_project = False
                    print(f"\tCheapestEmployeeScheduler.select_offer() selected wrong employees")

    if selects_correct:
        points += 0.4
    if correct_emps:
        points += 0.4
    if valid_project:
        points += 0.2

    if not has_result:
        points = 0.0

    print(f"Testing CheapestEmployeeScheduler finished: {points:.2f}/1 point")
    return points


def main():
    print("Testing Scheduler...")
    p1 = test_set_company()
    p2 = test_get_active_offers()
    p3 = test_get_new_project()
    p4 = test_FirstScheduler()
    p5 = test_RandomScheduler()
    p6 = test_GreedyScheduler()
    p7 = test_CheapestEmployeeScheduler()
    total = p1 + p2 + p3 + p4 + p5 + p6 + p7
    print(f"Testing Scheduler finished: {total:.2f}/3.5 points")
    print()
    print(f"SCHEDULER points: {total:.2f}/3.5 points")


if __name__ == '__main__':
    main()
