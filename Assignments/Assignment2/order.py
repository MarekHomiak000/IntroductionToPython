class Order:
    def __init__(self, client, offer, active, total_hours):
        self.client = client        #meno klienta ktory zadal zakazku (string)
        self.offer = offer          #cena zákazky (int/float)
        self.active = active        #číslo dňa, od ktorého bude zákazka aktuálna (int)
        self.total_hours = total_hours      #počet hodín potrebný pre vývoj zákazky (int)
        self.stages = {}      #rozdelenie hodín pre riešenie jednotlivých fáz projektu – dva kľúče: development a testing
        self.required_technologies = []     #zoznam jazykov a technológií, ktoré musia ovládať členovia riešiteľského tímu pre riešenie zákazky

    def set_tasks(self, development, testing):  # 0.2
        if development + testing != self.total_hours:
            raise ValueError("Your time for development and testing doesn't correspond with total_hours")

        if "development" not in self.stages and "testing" not in self.stages:
            self.stages["development"] = development
            self.stages["testing"] = testing

    def add_required_technologies(self, technologies):  # 0.2
        if isinstance(technologies, str) and technologies not in self.required_technologies:
            self.required_technologies.append(technologies)
        elif isinstance(technologies, list):
            self.required_technologies.extend(technologies)
        
        self.required_technologies = list(set(self.required_technologies))

    def get_offer(self):
        return self.offer

    def get_stages(self):
        return self.stages
    
    def get_technologies(self):
        return self.required_technologies
    
    def get_total_hours(self):
        return self.total_hours
    
    def get_client_name(self):
        return self.client

    def __str__(self):
        return f"Meno klienta: {self.client}, cena zakazky: {self.offer}, c. dna: {self.active}, pocet hodin: {self.total_hours}"


if __name__ == '__main__':
    # you can do some independent testing here
    order1 = Order("Blazej", 500, 2, 15)
    print(order1)

    order1.set_tasks(8,7)
    print(order1.get_stages())

    order1.add_required_technologies("Java")
    order1.add_required_technologies(["Python", "C", "Java", "Python"])
    print(order1.get_technologies())




