import pandas as pd

# Načítanie pickle súboru
df = pd.read_pickle(r"C:\Users\mHomi\Desktop\SKOLA\1_letny_semester\programovanie_v_pythone\Assignments\Assignment1\delayed_line.pkl")

# Uloženie do textového súboru s oddelenými hodnotami (napr. tabulátorom alebo čiarkou)
df = pd.DataFrame(df)
df.to_csv("xxx.txt", sep="\t", index=False)  # Použi "\t" pre tabulátor alebo "," pre čiarku
