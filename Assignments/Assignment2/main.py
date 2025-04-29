import random
import string

from company import *
from config import *
from employee import *
from order import *
from project import *
from scheduler import *


MANAGERS = 1
DEVELOPERS = 10
TESTERS = 6
TECHNOLOGIES = ['python', 'html', 'c#', 'java']
SCHED_TYPE = FirstScheduler


def generate_employees():
    emps = []
    for _ in range(MANAGERS):
        rand_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        level = random.choice(SENIORITY)
        wage = random.randint(WAGES[level][0], WAGES[level][1])
        emps.append(Manager(rand_name, level, wage))

    for _ in range(DEVELOPERS):
        rand_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        level = random.choice(SENIORITY)
        wage = random.randint(WAGES[level][0], WAGES[level][1])
        languages = random.sample(TECHNOLOGIES, 2)
        emps.append(Developer(rand_name, level, wage, languages))

    for _ in range(TESTERS):
        rand_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        level = random.choice(SENIORITY)
        wage = random.randint(WAGES[level][0], WAGES[level][1])
        emps.append(Tester(rand_name, level, wage))

    random.shuffle(emps)
    return emps


def generate_orders(n=30, sim_length=100):
    clients = [''.join(random.choice(string.ascii_uppercase)) for _ in range(5) for _ in range(int(n * 0.75))]

    orders = []
    for _ in range(n):
        hours = random.randint(2, 50) * 10
        avg_wage = random.randint(WAGES['junior'][0], WAGES['medior'][1])
        money = round(hours * avg_wage * 1.4)
        new_order = Order(
            client=random.choice(clients),
            offer=money,
            total_hours=hours,
            active=random.randint(1, sim_length - 20)  # gives time to finish all projects
        )
        tech_count = random.randint(1, 2)
        dev_time = round(hours * (random.random() * 0.6))
        new_order.set_tasks(dev_time, hours - dev_time)
        new_order.add_required_technologies(random.sample(TECHNOLOGIES, tech_count))

        orders.append(new_order)

    orders.sort(key=lambda o: o.active)
    return orders


def run_simulation(length=100):
    emps = generate_employees()
    orders = generate_orders(n=50, sim_length=length)
    scheduler = SCHED_TYPE(orders)
    company = Company(emps, scheduler)

    for day in range(1, length + 1):
        company.simulate_day(day)

    print(company.calculate_total_income())


if __name__ == '__main__':
    run_simulation(500)
