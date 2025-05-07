from employee import *
from order import *
from company import *
from scheduler import *

class Project:
    def __init__(self, company, order, started, employees):
        self.company = company          #firma, ktorá projekt rieši (Company)
        self.started = started          #deň v simulácii, kedy sa projekt začal riešiť (int)
        self.order = order              #zákazka, na základe ktorej vznikol projekt (Order)
        self.employees = find_employees(employees)          #zoznam zamestnancov, ktorí riešia projekt - okrem manažéra! (list)
        self.manager = find_manager(employees)              #manažér projektu - vždy len jeden! (Manager)
        self.remaining_hours = self.manager.get_project_time(self.order.get_total_hours())       #!!!DOPLNIT     počet hodín potrebných na dokončenie projektu (int)

        #pridanie do active_projects v company
        self.company.active_projects.append(self)

        for employee in self.employees:
            employee.curr_project = self
        self.manager.curr_project = self

    def update(self):
        self.remaining_hours -= len(self.employees) * 8
        if self.remaining_hours < 0:
            self.remaining_hours = 0

    def is_finished(self):
        return self.remaining_hours == 0

    def clear_project(self):
        for emp in self.employees:
            emp.curr_project = None
        self.manager.curr_project = None

        # odstránenie z active_projects cez identitu
        self.company.active_projects = [p for p in self.company.active_projects if p is not self]

        self.company.finished_projects.append(self)

    def get_income(self):
        # zisk pre tento projekt
        client = self.order.get_client_name()
        client_order_count = sum(1 for p in self.company.finished_projects if p.order.get_client_name() == client)

        offer = self.order.get_offer()
        if client_order_count >= 3:
            offer *= 1.5

        dev_time = self.manager.get_project_time(self.order.get_stages()["development"])
        test_time = self.manager.get_project_time(self.order.get_stages()["testing"])
        n_of_testers = n_of_devs = 0
        testers_wage = devs_wage = 0

        for emp in self.employees:
            if isinstance(emp, Tester):
                n_of_testers += 1
                testers_wage += emp.get_wage()
            elif isinstance(emp, Developer):
                n_of_devs += 1
                devs_wage += emp.get_wage()

        one_tester_hours = ceil(test_time / n_of_testers)
        one_dev_hours = ceil(dev_time / n_of_devs)

        total_wages = (one_tester_hours * testers_wage) + (one_dev_hours  * devs_wage)

        manager_hours = ceil((dev_time + test_time) / (n_of_devs + n_of_testers))
        manager_wage = self.manager.get_wage() * manager_hours

        total_expenses = manager_wage + total_wages
        income = offer - total_expenses

        return income

    
    def get_client_name(self):
        return self.order.get_client_name()
    
    def get_order(self):
        return self.order
    
    def __str__(self):
        emp_names = [emp.name for emp in self.employees]
        return f"Company name: {self.company}\nOrder: {self.order}\nStarted at day: {self.started}\nEmployees: {emp_names}\nManager: {self.manager.name}\nRem_time: {self.remaining_hours}"

    def __repr__(self):
        return f"Project for {self.order.get_client_name()}"
    
    def __eq__(self, other):
        if not isinstance(other, Project):
            return False
        return (self.company == other.company and 
                self.order == other.order and 
                self.started == other.started)

    def __hash__(self):
        return hash((self.company, self.order, self.started))
        

    



def find_employees(employees):
        employees_list = []
        for person in employees:
            if not isinstance(person, Manager):
                employees_list.append(person)
        return employees_list

def find_manager(employees):
        manager_list = []
        for person in employees:
            if isinstance(person, Manager):
                manager_list.append(person)
        
        if len(manager_list) != 1:
            raise ValueError("More or less managers than it shoud be")
        else:
            return manager_list[0]
        


if __name__ == '__main__':
    # you can do some independent testing here
    tester1 = Tester("tester1_Milos", "junior", 20)
    tester2 = Tester("tester2_Bohus", "medior", 25)
    developer1 = Developer("dev1_Jozo", "medior", 30, ["Rust", "C", "Python", "Java"])
    developer2 = Developer("dev2_Jano", "senior", 30, ["Javascript"])
    developer3 = Developer("dev3_Vojta", "junior", 20, ["C"])
    manager1 = Manager("manager1_Hugo", "senior", 50)
    employees_lst = [tester1, developer1, developer2, manager1, tester2, developer3]

    scheduler = Scheduler([1,2,3])
    firma1 = Company(employees_lst, scheduler)

    for i in employees_lst:
        print(i)

    order1 = Order("Blazej", 5000, 2, 200)
    order2 = Order("Blazej", 5000, 2, 200)
    #order3 = Order("Blazej", 5000, 2, 200)
    print(order1)

    print()

    project1 = Project(firma1, order1, 5, employees_lst)
    project2 = Project(firma1, order2, 5, employees_lst)
    #project3 = Project(firma1, order3, 5, employees_lst)
    print(project1)

    print()

    project1.order.set_tasks(100,100)
    project2.order.set_tasks(100,100)
    #project3.order.set_tasks(100,100)
    print(project1.order.get_stages())

    project1.clear_project()
    project2.clear_project()
    #project3.clear_project()

    print(firma1.get_finished_projects())

    print(project2.get_income())

  

    


