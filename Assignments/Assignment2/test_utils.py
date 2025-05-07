import random
import string

import config as st_conf
import company as st_comp
import employee as st_emp
import order as st_ord
import project as st_proj
import scheduler as st_sched


def get_random_letter(letters):
    return random.choice(letters)


def generate_name(n):
    name = get_random_letter(string.ascii_uppercase)
    for _ in range(n - 1):
        name += get_random_letter(string.ascii_lowercase)
    return name


def generate_random_employee(emp_type):
    name = generate_name(5) + " " + generate_name(7)
    level = random.choice(st_conf.SENIORITY)
    wage = round(random.uniform(st_conf.WAGES[level][0], st_conf.WAGES[level][1]), 2)

    if emp_type == st_emp.Developer:
        langs = random.sample(['html', 'python', 'C#', 'C++'], 2)
        return emp_type(name, level, wage, langs)

    return emp_type(name, level, wage)


def generate_random_order():
    client_name = generate_name(8)
    offer = random.randint(1, 20) * 1000
    active = random.randint(1, 10)
    total_hours = round((offer // 20) * random.uniform(0.8, 1.2))

    return st_ord.Order(client_name, offer, active, total_hours)


def generate_random_company(employee_count, sched_type, order_count=0, set_company=False):
    orders = [generate_random_order() for _ in range(order_count)]
    sched = sched_type(orders)

    emps = [generate_random_employee(st_emp.Developer) for _ in range(int(employee_count * 0.4))]
    emps += [generate_random_employee(st_emp.Tester) for _ in range(int(employee_count * 0.4))]
    emps += [generate_random_employee(st_emp.Manager) for _ in range(int(employee_count * 0.2))]

    company = st_comp.Company(emps, sched)
    if set_company:
        sched.company = company

    return company


def get_project_employees(emp_list):
    managers = [emp for emp in emp_list if isinstance(emp, st_emp.Manager)]
    testers = [emp for emp in emp_list if isinstance(emp, st_emp.Tester)]
    devs = [emp for emp in emp_list if isinstance(emp, st_emp.Developer)]

    selection = [random.choice(managers)]
    selection += random.sample(testers, random.randint(1, len(testers)))
    selection += random.sample(devs, random.randint(1, len(devs)))

    random.shuffle(selection)

    return selection


if __name__ == '__main__':
    for _ in range(10):
        # print(generate_random_order())
        print(generate_random_company(10, st_sched.RandomScheduler))
