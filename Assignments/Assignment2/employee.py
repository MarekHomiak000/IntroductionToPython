from config import SENIORITY as seniority
from config import WAGES as wages_dict
from math import ceil

class Employee:
    def __init__(self, name, level, wage):
        self.name = name
        self.level = validuj_level(level)
        self.wage = validuj_plat(wage, level)
        self.curr_project = None
    
    def get_wage(self):
        return self.wage
    
    def get_curr_p(self):
        return self.curr_project
    
    def __str__(self):
        return f"EMPLOYEE - Meno: {self.name}, level: {self.level}, wage: {self.wage}"

class Tester(Employee):
    def __init__(self, name, level, wage):
        super().__init__(name, level, wage)

    def __str__(self):
        return f"TESTER - Meno: {self.name}, level: {self.level}, wage: {self.wage}"
    
    def __repr__(self):
        return f"{self.name}"


class Developer(Employee):
    def __init__(self, name, level, wage, languages):
        super().__init__(name, level, wage)
        self.languages = languages

    def can_program(self, language):
        return language in self.languages

    def __str__(self):
        return f"DEVELOPER - Meno: {self.name}, level: {self.level}, wage: {self.wage}"
    
    def __repr__(self):
        return f"{self.name}"


class Manager(Employee):
    def __init__(self, name, level, wage):
        super().__init__(name, level, wage)

    def get_project_time(self, orig_time):
        if self.level == "junior":
            return int(ceil(orig_time * 1.2))
        elif self.level == "senior":
            return int(ceil(orig_time * 0.8))
        else:
            return int(ceil(orig_time))
    
    def __str__(self):
        return f"MANAGER - Meno: {self.name}, level: {self.level}, wage: {self.wage}"
    
    def __repr__(self):
        return f"{self.name}"




def validuj_plat(wage, level):
        if not isinstance(wage, (int, float)):
            raise TypeError(f"Incorrect wage type: {type(wage)}")
        
        min_wage, max_wage = wages_dict[level]
        if wage < min_wage or wage > max_wage:
            raise ValueError(f"Incorrect wage for {level} worker: {wage}")
        
        return wage

def validuj_level(level):
        if level not in seniority:
            raise ValueError(f"Unknown seniority level {level}")
        
        return level

if __name__ == '__main__':
    employee1 = Employee("Andrej", "senior", 30)
    tester1 = Tester("Milos", "junior", 20)
    developer1 = Developer("Dodo", "medior", 20, ["Rust", "C", "Python", "Java"])
    manager1 = Manager("Hugo", "senior", 50)

    print(employee1)
    print(tester1)
    print(f"{developer1} : can program in Python? {developer1.can_program("Python")}")
    print(f"{manager1} - time in which he can make work: {manager1.get_project_time(50)}")
    