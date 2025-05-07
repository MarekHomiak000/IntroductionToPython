# Meno: Homiak, Marek
# Spolupráca: 
# Použité zdroje: 
# Čas: 

# Podrobný popis je dostupný na: https://github.com/ianmagyar/introduction-to-python/blob/master/homeworks/homework07.md

# Hodnotenie: /1b

# TODO: add your definition of the class

class TUKEStudent:
    university = "TUKE"
    def __init__(self, name, isic):
        self.name = name
        self.__isic_num = isic
    
    def get_ISIC(self):
        return self.__isic_num
    
    def __eq__(self, other):
        if isinstance(other, TUKEStudent):
            return self.__isic_num == other.__isic_num
        return False