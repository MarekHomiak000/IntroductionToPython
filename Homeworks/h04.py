# -*- coding: utf-8 -*-

# Meno: Homiak, Marek
# Spolupráca: 
# Použité zdroje: 
# Čas: 

# Podrobný popis je dostupný na: https://github.com/ianmagyar/introduction-to-python/blob/master/homeworks/homework04.md

# Hodnotenie: /1b

import numpy
import pandas

# --------------------
# Úloha 1
# Načítajte dataset uložený v súbore h04.csv ako pandas DataFrame
# a určte pomocou metód pandas dataframe (alebo cez použitie numpy poľa):
#  - meno najťažšej ženy v datasete
df = pandas.read_csv('h04.csv')
women_df = df[df['gender'] == 'F']
max_weight_index = women_df['weight'].idxmax()
heaviest_woman_name = women_df.loc[max_weight_index, 'name']

print(f"Meno najťažšej ženy v datasete je: {heaviest_woman_name}")


# --------------------
# Úloha 2
# V kóde nižšie sa vygeneruje dvojrozmerné numpy pole s náhodnými číselnými
# hodnotami. Vypočítajte:
#  - strednú hodnotu (medián) po riadkoch
array = numpy.random.rand(5, 5)
print(array)

row_medians = numpy.median(array, axis=1)
print("Medián po riadkoch:")
print(row_medians)
