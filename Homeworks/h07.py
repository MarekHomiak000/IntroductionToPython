# Meno: Homiak, Marek
# Spolupráca: 
# Použité zdroje: 
# Čas: 

# Podrobný popis je dostupný na: https://github.com/ianmagyar/introduction-to-python/blob/master/homeworks/homework07.md

# Hodnotenie: /1b

# TODO: add your definition of the class

class Singer:
    def __init__(self, name, band, band_role):
        self.name = name
        self.__band = band
        self.band_role = band_role
    
    def change_band(self, new_band):
        self.__band = new_band

    def get_band_role(self):
        return self.band_role
    
    def __str__(self):
        return f"{self.name} is a {self.band_role} in {self.__band}"

Person1 = Singer("Jozko", "ACDC", "guitarist")
print(Person1)

Person1.change_band("Metallica")
print(Person1)