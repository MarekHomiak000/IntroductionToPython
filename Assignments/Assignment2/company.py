from employee import *
from order import *
from company import *
from scheduler import *
from project import Project

class Company:
    def __init__(self, employees, scheduler):
        self.employees = employees
        self.active_projects = []
        self.finished_projects = []
        self.scheduler = scheduler
        self.scheduler.set_company(self)

    def calculate_total_income(self):
        total_income = 0
        for project in self.finished_projects:
            total_income += project.get_income()
        return total_income

    def get_available_employees(self, emp_type):
        return [w for w in self.employees if isinstance(w, emp_type) and w.get_curr_p() == None]

    def get_lang_developers(self, language):
        devs = []
        for emp in self.employees:
            if isinstance(emp, Developer) and emp.can_program(language):
                devs.append(emp)
        return devs

    def is_frequent_client(self, client_name):
        count = 0
        for p in self.finished_projects:
            name = p.get_client_name()
            if name == client_name:
                count += 1
        return count >= 3

    def close_project(self, project):
        for p in self.active_projects:
            if p == project:
                self.finished_projects.append(p)
                self.active_projects.remove(p)
        else:
            pass

    def solving(self, order):
        for o in self.finished_projects:
            if o.get_order() == order:
                return True
        for o in self.active_projects:
            if o.get_order() == order:
                return True
        return False

    def can_solve_order(self, order):
        free_managers = self.get_available_employees(Manager)
        free_devs = self.get_available_employees(Developer)
        free_testers = self.get_available_employees(Tester)

        #return f"avab managers: {free_managers}\navab devs: {free_devs}\navab testers: {free_testers}"

        #musí byť dostupný aspoň jeden manažér
        managers_bool = False
        if len(free_managers) > 0:
            managers_bool = True

        #pre každú potrebnú technológiu musí byť dostupný aspoň jeden vývojár
        #TODO (ale funguje aj bez toho)

        #počet dostupných vývojárov musí byť aspoň rovný počtu požadovaných technológií 
        devs_bool = False
        if len(free_devs) >= len(order.get_technologies()):
            devs_bool = True

        #k zákazka vyžaduje testovanie, musí byť dostupný aspoň jeden tester
        testing_bool = False
        if order.get_stages()["testing"] > 0 and len(free_testers) > 0:
            testing_bool = True

        return managers_bool and testing_bool and devs_bool
        

    def simulate_day(self, day_no):
        pass

    def __str__(self):
        return f"Total income: {self.calculate_total_income()}, Devs: {self.get_lang_developers("Python")}"
    
    def __repr__(self):
        return f"Company(employees={self.employees}, active_projects={self.active_projects})"

    def get_employees(self): 
        return f"{self.employees}"
    
    def get_active_projects(self): 
        return self.active_projects
    
    def get_finished_projects(self): 
        return self.finished_projects
    

if __name__ == '__main__':
    # you can do some independent testing here
    tester1 = Tester("tester1_Milos", "junior", 20)
    tester2 = Tester("tester2_Bohus", "medior", 25)
    tester3 = Tester("tester2_Milan", "junior", 15)
    developer1 = Developer("dev1_Jozo", "medior", 30, ["Rust", "C", "Python", "Java"])
    developer2 = Developer("dev2_Jano", "senior", 30, ["Javascript"])
    developer3 = Developer("dev3_Vojta", "junior", 20, ["C", "Python"])
    manager1 = Manager("manager1_Hugo", "senior", 50)
    manager2 = Manager("manager1_Mirko", "senior", 48)
    employees_lst = [tester1, developer1, developer2, manager1, tester2, developer3, tester3, manager2]

    scheduler = Scheduler([1,2,3])
    company = Company(employees_lst, scheduler)

    for emp in employees_lst:
        print(emp)
    print()

    #OBJEDNAVKA 1
    order1 = Order("Blazej", 5000, 1, 100)
    #print(f"OBJEDNAVKA1: {order1}\n")
    needed_employees = [tester1, tester2, developer1, developer2, manager1]
    project1 = Project(company, order1, 1, needed_employees)
    #print(f"PROJEKT1: {project1}")
    project1.order.set_tasks(80,20)

    #company.close_project(project1)
    project1.clear_project()

    #OBJEDNAVKA 2
    order2 = Order("Stevko", 10000, 1, 300)
    #print(f"OBJEDNAVKA2: {order2}\n")
    needed_employees = [tester1, tester2, tester3, developer1, developer2, developer3, manager1]
    project2 = Project(company, order2, 1, needed_employees)
    #print(f"PROJEKT2: {project2}")
    project2.order.set_tasks(100,200)

    #company.close_project(project2) 
    project2.clear_project()

    

    #OBJEDNAVKA 3
    order3 = Order("Pista", 100000, 1, 1000)
    order3.add_required_technologies(["Java"])
    print(f"OBJEDNAVKA3: {order1}\n")
    needed_employees = [tester1, developer1, developer2, manager1]
    project3 = Project(company, order3, 1, needed_employees)
    print(f"PROJEKT3: {project3}")
    project3.order.set_tasks(700,300)

    #company.close_project(project3)
    #project3.clear_project()


    print(f"Income: {project3.get_income()}") 


    print(f"\nactive_projects: {company.get_active_projects()}")
    print(f"finished_projects: {company.get_finished_projects()}")

    print(f"\n{company}")
    print(f"devs: {company.get_lang_developers("Python")}")

    order4 = Order("Test", 100000, 1, 1000)
    print(f"\nSolving: {company.solving(order4)}")

    print(f"\n{company.can_solve_order(order3)}")

    #
    #TODO odrazka 2 a 4 v COMPANY can_solve_order
    #
