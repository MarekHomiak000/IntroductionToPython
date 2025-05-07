import math
import random

import company as st_comp
import employee as st_emp
import order as st_ord
import project as st_proj
import scheduler as st_sched

from test_utils import *


def test_structure(obj, should_have):
    attribute_list = dir(obj)
    for att in should_have:
        if att not in attribute_list:
            print(f"\tMissing attribute {att} in object {obj}. (Found attributes {attribute_list})")
    else:
        return True
    return False


def project_setup():
    test_company = generate_random_company(20, st_sched.RandomScheduler, order_count=0, set_company=True)
    test_order = generate_random_order()
    test_started = 1
    comp_emps = test_company.employees
    managers = [emp for emp in comp_emps if isinstance(emp, st_emp.Manager)]
    testers = [emp for emp in comp_emps if isinstance(emp, st_emp.Tester)]
    devs = [emp for emp in comp_emps if isinstance(emp, st_emp.Developer)]

    manager = [random.choice(managers)]
    devs = random.sample(devs, random.randint(1, len(devs)))
    testers = random.sample(testers, random.randint(1, len(testers)))
    test_employees = manager + devs + testers
    random.shuffle(test_employees)

    test_project = st_proj.Project(test_company, test_order, test_started, test_employees)
    
    return test_project, manager, devs, testers, test_company, test_order


def test_project_constructor():
    print("Testing Project constructor...")
    points = 0.0

    for _ in range(8):
        try:
            test_project, test_manager, test_devs, test_testers, test_company, test_order = project_setup()
        except Exception as e:
            print("\tCalling Project constructor caused an unexpected error:")
            print(e)
        else:
            if test_structure(test_project,
                              ['company', 'started', 'order', 'manager', 'employees', 'remaining_hours']):
                points += 0.1

                if test_project.company != test_company:
                    print(f"\tProject.company should be {test_company}, found {test_project.company}")
                else:
                    points += 0.05
                if test_project.started != 1:
                    print(f"\tProject.started should be 1, found {test_project.started}")
                else:
                    points += 0.05
                if test_project.order != test_order:
                    print(f"\tProject.order should be {test_order}, found {test_project.order}")
                else:
                    points += 0.05

                correct_hours = test_order.total_hours
                if test_manager[0].level == 'senior':
                    correct_hours = math.ceil(correct_hours * 0.8)
                if test_manager[0].level == 'junior':
                    correct_hours = math.ceil(correct_hours * 1.2)
                if test_project.remaining_hours != correct_hours:
                    print(f"\tProject.remaining_hours should be {correct_hours}, found {test_project.remaining_hours}")
                else:
                    points += 0.05

                if test_project.manager != test_manager[0]:
                    print(f"\tProject.manager should be {test_manager[0]}, found {test_project.manager}")
                else:
                    points += 0.05
                if test_project.manager.curr_project != test_project:
                    print(f"\tProject.manager current project not set")
                else:
                    points += 0.05

                for emp in test_devs + test_testers:
                    if emp not in test_project.employees:
                        print(f"\tMissing employee {emp} in Project.employee")
                        break
                else:
                    points += 0.05

                for emp in test_devs + test_testers:
                    if emp.curr_project != test_project:
                        print(f"\tEmployee {emp} current project not set")
                        break
                else:
                    points += 0.05

    points /= 10

    # error when multiple managers
    test_company = generate_random_company(20, st_sched.RandomScheduler, order_count=0, set_company=True)
    test_order = generate_random_order()
    test_started = 1
    comp_emps = test_company.employees
    managers = [emp for emp in comp_emps if isinstance(emp, st_emp.Manager)]
    testers = [emp for emp in comp_emps if isinstance(emp, st_emp.Tester)]
    devs = [emp for emp in comp_emps if isinstance(emp, st_emp.Developer)]

    manager = managers
    devs = random.sample(devs, random.randint(1, len(devs)))
    testers = random.sample(testers, random.randint(1, len(testers)))
    test_employees = manager + devs + testers
    random.shuffle(test_employees)

    try:
        test_project = st_proj.Project(test_company, test_order, test_started, test_employees)
    except ValueError:
        points += 0.05
    except Exception:
        print("\tProject constructor should raise ValueError when too many managers are given")
    else:
        print("\tProject constructor should raise ValueError when too many managers are given")


    # error when manager is missing
    test_company = generate_random_company(20, st_sched.RandomScheduler, order_count=0, set_company=True)
    test_order = generate_random_order()
    test_started = 1
    comp_emps = test_company.employees
    managers = [emp for emp in comp_emps if isinstance(emp, st_emp.Manager)]
    testers = [emp for emp in comp_emps if isinstance(emp, st_emp.Tester)]
    devs = [emp for emp in comp_emps if isinstance(emp, st_emp.Developer)]

    manager = []
    devs = random.sample(devs, random.randint(1, len(devs)))
    testers = random.sample(testers, random.randint(1, len(testers)))
    test_employees = manager + devs + testers
    random.shuffle(test_employees)

    try:
        test_project = st_proj.Project(test_company, test_order, test_started, test_employees)
    except ValueError:
        points += 0.05
    except Exception:
        print("\tProject constructor should raise ValueError when no manager is given")
    else:
        print("\tProject constructor should raise ValueError when no manager is given")

    print(f"Testing Project constructor finished: {points:.2f}/0.5 points")
    return points


def test_update():
    print("Testing Project.update()...")
    points = 0.0

    for _ in range(4):
        test_project, test_manager, test_devs, test_testers, test_company, test_order = project_setup()
        emp_count = len(test_devs) + len(test_testers)
        
        for _ in range(5):
            prev_val = test_project.remaining_hours
            try:
                test_project.update()
            except Exception as e:
                print("\tCalling Project.update() casued an unexpected error:")
                print(e)
            else:
                new_val = test_project.remaining_hours
                corr_val = max(0, prev_val - emp_count * 8)
                if new_val != corr_val:
                    print(f"\tProject.update() updated remaining_hours incorrectly: expected {corr_val}, found {new_val}")
                else:
                    points += 0.01

    print(f"Testing Project.update() finished: {points:.2f}/0.2 points")
    return points


def test_is_finished():
    print("Testing Project.is_finished()...")
    points = 0.0

    for _ in range(10):
        test_project, test_manager, test_devs, test_testers, test_company, test_order = project_setup()
        test_project.remaining_hours = random.randint(1, 500)

        try:
            st_res = test_project.is_finished()
        except Exception as e:
            print("\tCalling Project.is_finished() casued an unexpected error:")
            print(e)
        else:
            if not st_res:
                points += 0.005
            else:
                print("Project.is_finished() should return False if there are still hours remaining")

    test_project, test_manager, test_devs, test_testers, test_company, test_order = project_setup()
    test_project.remaining_hours = 0

    try:
        st_res = test_project.is_finished()
    except Exception as e:
        print("\tCalling Project.is_finished() casued an unexpected error:")
        print(e)
    else:
        if st_res:
            points += 0.05
        else:
            print("Project.is_finished() should return True if there are no hours remaining")

    print(f"Testing Project.is_finished() finished: {points:.2f}/0.1 point")
    return points


def test_clear_project():
    print("Testing Project.clear_project()...")
    points = 0.0

    test_project, test_manager, test_devs, test_testers, test_company, test_order = project_setup()
    test_company.active_projects.append(test_project)

    try:
        test_project.clear_project()
    except Exception as e:
        print("\tCalling Project.clear_project() casued an unexpected error:")
        print(e)
    else:
        if test_project not in test_company.finished_projects:
            print("\tProject was not moved to finished projects")
        else:
            points += 0.05

        if test_project in test_company.active_projects:
            print("\tProject still in active projects")
        else:
            points += 0.05

        for emp in test_manager + test_devs + test_testers:
            if emp.curr_project is not None:
                print(f"\tProject was not cleared for employee {emp}")
                break
        else:
            points += 0.1

    print(f"Testing Project.clear_project() finished: {points:.2f}/0.2 points")
    return points


def test_get_income_no_bonus_case1():
    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    order = st_ord.Order("ClientA", 10000, 1, 100)
    order.set_tasks(60, 40)

    dev = st_emp.Developer("Dev", "junior", 20, ["Python"])
    tester = st_emp.Tester("Test", "junior", 20)
    manager = st_emp.Manager("Man", "junior", 20)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 6400


def test_get_income_no_bonus_case2():
    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    order = st_ord.Order("ClientB", 15000, 1, 150)
    order.set_tasks(90, 60)

    dev = st_emp.Developer("Dev", "medior", 30, ["Python"])
    tester = st_emp.Tester("Test", "junior", 20)
    manager = st_emp.Manager("Man", "junior", 20)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 8520


def test_get_income_no_bonus_case3():
    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    order = st_ord.Order("ClientC", 8000, 1, 80)
    order.set_tasks(50, 30)

    dev = st_emp.Developer("Dev", "medior", 25, ["Python"])
    tester = st_emp.Tester("Test", "medior", 25)
    manager = st_emp.Manager("Man", "senior", 50)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 4800


def test_get_income_no_bonus_case4():
    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    order = st_ord.Order("ClientD", 12000, 1, 120)
    order.set_tasks(70, 50)

    dev = st_emp.Developer("Dev", "senior", 40, ["Python"])
    tester = st_emp.Tester("Test", "junior", 20)
    manager = st_emp.Manager("Man", "medior", 30)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 6400


def test_get_income_no_bonus_case5():
    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    order = st_ord.Order("ClientE", 9000, 1, 90)
    order.set_tasks(40, 50)

    dev = st_emp.Developer("Dev", "junior", 15, ["Python"])
    tester = st_emp.Tester("Test", "senior", 35)
    manager = st_emp.Manager("Man", "junior", 20)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 5100


def test_get_income_with_bonus_case1():
    dev = st_emp.Developer("Dev", "junior", 20, ["Python"])
    tester = st_emp.Tester("Test", "junior", 20)
    manager = st_emp.Manager("Man", "junior", 20)

    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    for _ in range(3):
        company.finished_projects.append(st_proj.Project(company, st_ord.Order("ClientX", 5000, 1, 50), 1, [manager, dev, tester]))

    order = st_ord.Order("ClientX", 10000, 1, 100)
    order.set_tasks(60, 40)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 11400


def test_get_income_with_bonus_case2():
    dev = st_emp.Developer("Dev", "medior", 30, ["Python"])
    tester = st_emp.Tester("Test", "junior", 20)
    manager = st_emp.Manager("Man", "junior", 20)

    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    for _ in range(3):
        company.finished_projects.append(st_proj.Project(company, st_ord.Order("ClientY", 3000, 1, 30), 1, [manager, dev, tester]))

    order = st_ord.Order("ClientY", 15000, 1, 150)
    order.set_tasks(90, 60)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 16020


def test_get_income_with_bonus_case3():
    dev = st_emp.Developer("Dev", "medior", 25, ["Python"])
    tester = st_emp.Tester("Test", "medior", 25)
    manager = st_emp.Manager("Man", "senior", 50)

    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    for _ in range(3):
        company.finished_projects.append(st_proj.Project(company, st_ord.Order("ClientZ", 7000, 1, 70), 1, [manager, dev, tester]))

    order = st_ord.Order("ClientZ", 8000, 1, 80)
    order.set_tasks(50, 30)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 8800


def test_get_income_with_bonus_case4():
    dev = st_emp.Developer("Dev", "senior", 40, ["Python"])
    tester = st_emp.Tester("Test", "junior", 20)
    manager = st_emp.Manager("Man", "medior", 30)

    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    for _ in range(3):
        company.finished_projects.append(st_proj.Project(company, st_ord.Order("ClientA", 2000, 1, 20), 1, [manager, dev, tester]))

    order = st_ord.Order("ClientA", 12000, 1, 120)
    order.set_tasks(70, 50)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 12400


def test_get_income_with_bonus_case5():
    dev = st_emp.Developer("Dev", "junior", 15, ["Python"])
    tester = st_emp.Tester("Test", "senior", 35)
    manager = st_emp.Manager("Man", "junior", 20)

    sched = st_sched.RandomScheduler([])
    company = st_comp.Company([], sched)
    for _ in range(3):
        company.finished_projects.append(st_proj.Project(company, st_ord.Order("ClientE", 1000, 1, 10), 1, [manager, dev, tester]))

    order = st_ord.Order("ClientE", 9000, 1, 90)
    order.set_tasks(40, 50)

    project = st_proj.Project(company, order, 1, [manager, dev, tester])
    company.finished_projects.append(project)

    return project, 9600

def test_get_income():
    print("Testing Project.clear_project()...")
    points = 0.0

    proj1, res1 = test_get_income_no_bonus_case1()
    try:
        st_res = proj1.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res1:
            points += 0.1
        else:
            print(f"No bonus test case 1 failed. Expected {res1}, got {st_res}")

    proj2, res2 = test_get_income_no_bonus_case2()
    try:
        st_res = proj2.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res2:
            points += 0.1
        else:
            print(f"No bonus test case 2 failed. Expected {res2}, got {st_res}")

    proj3, res3 = test_get_income_no_bonus_case3()
    try:
        st_res = proj3.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res3:
            points += 0.1
        else:
            print(f"No bonus test case 3 failed. Expected {res3}, got {st_res}")

    proj4, res4 = test_get_income_no_bonus_case4()
    try:
        st_res = proj4.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res4:
            points += 0.1
        else:
            print(f"No bonus test case 4 failed. Expected {res4}, got {st_res}")

    proj5, res5 = test_get_income_no_bonus_case5()
    try:
        st_res = proj5.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res5:
            points += 0.1
        else:
            print(f"No bonus test case 5 failed. Expected {res5}, got {st_res}")

    proj1, res1 = test_get_income_with_bonus_case1()
    try:
        st_res = proj1.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res1:
            points += 0.1
        else:
            print(f"Bonus test case 1 failed. Expected {res1}, got {st_res}")

    proj2, res2 = test_get_income_with_bonus_case2()
    try:
        st_res = proj2.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res2:
            points += 0.1
        else:
            print(f"Bonus test case 2 failed. Expected {res2}, got {st_res}")

    proj3, res3 = test_get_income_with_bonus_case3()
    try:
        st_res = proj3.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res3:
            points += 0.1
        else:
            print(f"Bonus test case 3 failed. Expected {res3}, got {st_res}")

    proj4, res4 = test_get_income_with_bonus_case4()
    try:
        st_res = proj4.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res4:
            points += 0.1
        else:
            print(f"Bonus test case 4 failed. Expected {res4}, got {st_res}")

    proj5, res5 = test_get_income_with_bonus_case5()
    try:
        st_res = proj5.get_income()
    except Exception as e:
        print("\tCalling Project.get_income() caused an unexpected exception")
        print(e)
    else:
        if st_res == res5:
            points += 0.1
        else:
            print(f"Test case 5 failed. Expected {res5}, got {st_res}")

    print(f"Testing Project.clear_project() finished: {points:.2f}/1 point")
    return points


def main():
    print("Testing Project...")
    p1 = test_project_constructor()
    p2 = test_update()
    p3 = test_is_finished()
    p4 = test_clear_project()
    p5 = test_get_income()
    total = p1 + p2 + p3 + p4 + p5
    print(f"Testing Project finished: {total:.2f}/2 points")
    print()
    print(f"PROJECT points: {total:.2f}/2 points")


if __name__ == '__main__':
    main()
