from gettext import npgettext
import sys
import os

print(os.getcwd())
print(sys.argv)

args = sys.argv

if len(args) > 1:
    print('Skriptui buvo pateikti \nparametrai')


    #parašykite skriptą, kuriam galėtumėte nurodyti tris argumentus,
    #  du skaičius ir matematinį veiksmą. Skriptas turi išspausdinti 
    # rezultatą. Nuspręskite, ką darysite, jei bus pateikta per daug,
    #  per mažai, ar netinkami parametrai


import sys

def calculiatorius(num1, operator, num2):
    try:
        
        num1 = float(num1)
        num2 = float(num2)

        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Klaida: Dalyba is nulio negalima."
            return num1 / num2
        else:
            return "Klaida: Netinkamas operatorius. Galimi operatoriai: +, -, *, /"
    except ValueError:
        return "Klaida: Abu argumentai turi buti skaiciai."

def main():
    if len(sys.argv) != 4:
        print("Klaida: Turite pateikti tris argumentus. Pvz: 5 + 3")
        return
    
    num1 = sys.argv[1]
    operator = sys.argv[2]
    num2 = sys.argv[3]

    result = calculiatorius(num1, operator, num2)
    print(f"Rezultatas: {result}")

if __name__ == "__main__":
    main()


import sys
import os
import matplotlib.pyplot as plt
import numpy as np

A = np.arange(0, 10)
B = A*np.random.randint(1,11,10)
C = B*np.random.randint(1,11,10)

fig, ax = plt.subplots()
ax.plot(A,B)
plt.show()

fig, ax = plt.subplots()
ax.plot(A,C)
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_data(filenames, separator, columns):
    plt.figure(figsize=(10, 6))

    for file in filenames:
        try:
            data = pd.read_csv(file, sep=separator)

            if not all(col in data.columns for col in columns):
                print(f"Klaida: Kai kurie nurodyti stulpeliai nerasti faile {file}. Galimi stulpeliai: {data.columns.tolist()}")
                continue

            
            data[columns].plot(label=file)

        except Exception as e:
            print(f"Klaida nuskaitant faila {file}: {e}")
            continue
    plt.title("Failų duomenu palyginimas")
    plt.xlabel(columns[0])
    plt.ylabel(", ".join(columns[1:]))
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    if len(sys.argv) < 5:
        print("Klaida: Turite nurodyti bent viena faila, skirtuka ir stulpelius.")
        return

    
    files = sys.argv[1:-2]
    separator = sys.argv[-2]
    columns = sys.argv[-1].split(',')

    plot_data(files, separator, columns)

if __name__ == "__main__":
    main()



# .iloc[:, 1]