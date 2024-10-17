import sys
import os

#parašykite skriptą, kuriam galėtumėte nurodyti tris argumentus,
# du skaičius ir matematinį veiksmą. Skriptas turi išspausdinti rezultatą.
# Nuspręskite, ką darysite, jei bus pateikta per daug, per mažai, ar netinkami parametrai.


args = sys.argv
print(args)
# if len(args) > 1:
#     print('sriptui buvo pateikti\nparametrai')
#     print(f'ju kiekis {len(args) -1}')

# if len(args) < 4:
#     print('per mazai argumentu')
# elif len(args) > 4:
#     print('per daug argumentu')
# elif args[-1] not in ('+-/*%**'):
#     print('neteisinga tvarka nurydyti elementai: du skaiciai ir simbolis')
# else:
#     if args[-1] == '+':
#         ans = float(args[1])+float(args[2])
#     elif args[-1] == '-':
#         ans = float(args[1])*float(args[2])
#     elif args[-1] == '/':
#         ans = float(args[1])/float(args[2])
#     elif args[-1] == '*':
#         ans = float(args[1])*float(args[2])
#     elif args[-1] == '**':
#         ans = float(args[1])**float(args[2])
#     elif args[-1] == '%':
#         ans = float(args[1])%float(args[2])
    
#     print(f'rezultatas: {ans}')