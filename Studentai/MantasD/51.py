import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
# Failo pavadinime yra specifinis kodas (D_5k, D_2k, B_1k, ir taip toliau). Pagal ansktesnį pavyzdį
# matyti, jog taip paprastai atrenkant - tas trumpinys pakinta
# pakeiskite skriptą taip, kad
# jei jūsų skriptas rado, kad pavyzdžiui, DAY0 geriausias REF yra su kodu D_5k, tai
# DAY1 ir DAY2 turi būti vaizduojami duomenys iš failų su tuo pat kodu (D_5k pavyzdžiui)
def get_file_by_min_val(location, column):
    import pandas as pd
    import glob
    dat_failai = glob.glob(location)
    files = []
    min_p = []
    for file in dat_failai:
        df = pd.read_csv(file, delimiter=';')
        min_p.append(min(list(df[column])))
        files.append(file)
        
    for file, val in zip(files,min_p):
        if val == min(min_p):
            f = file.split('/')[-1]
            s = '_'.join(f.split('\\')[1].split('_')[:3])
            return [file, round(val*-1,2), f, s]
        
# REF
file_day0 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY0/REF*.dat',' P[mW/cm^2]')
file_day1 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY1/REF*.dat',' P[mW/cm^2]')
file_day2 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY2/REF*.dat',' P[mW/cm^2]')
df_day0 = pd.read_csv(file_day0[0], delimiter=';')
df_day1 = pd.read_csv(file_day1[0], delimiter=';')
df_day2 = pd.read_csv(file_day2[0], delimiter=';')
df_day0['j']= df_day0[' j[mA/cm^2] '].apply(lambda x: x*-1)
df_day0['Type']= df_day0[' j[mA/cm^2] '].apply(lambda x: f"DAY0 {file_day0[2]} {file_day0[1]}%")
df_day1['j']= df_day1[' j[mA/cm^2] '].apply(lambda x: x*-1)
df_day1['Type']= df_day1[' j[mA/cm^2] '].apply(lambda x: f"DAY1 {file_day1[2]} {file_day1[1]}%")
df_day2['j']= df_day2[' j[mA/cm^2] '].apply(lambda x: x*-1)
df_day2['Type']= df_day2[' j[mA/cm^2] '].apply(lambda x: f"DAY2 {file_day2[2]} {file_day2[1]}%")
df = pd.concat([df_day0,df_day1,df_day2])
# V1145
file1_day0 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY0/V1145*.dat',' P[mW/cm^2]')
file1_day1 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY1/V1145*.dat',' P[mW/cm^2]')
file1_day2 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY2/V1145*.dat',' P[mW/cm^2]')
df1_day0 = pd.read_csv(file1_day0[0], delimiter=';')
df1_day1 = pd.read_csv(file1_day1[0], delimiter=';')
df1_day2 = pd.read_csv(file1_day2[0], delimiter=';')
df1_day0['j']= df1_day0[' j[mA/cm^2] '].apply(lambda x: x*-1)
df1_day0['Type']= df1_day0[' j[mA/cm^2] '].apply(lambda x: f"DAY0 {file1_day0[2]} {file1_day0[1]}%")
df1_day1['j']= df1_day1[' j[mA/cm^2] '].apply(lambda x: x*-1)
df1_day1['Type']= df1_day1[' j[mA/cm^2] '].apply(lambda x: f"DAY1 {file1_day1[2]} {file1_day1[1]}%")
df1_day2['j']= df1_day2[' j[mA/cm^2] '].apply(lambda x: x*-1)
df1_day2['Type']= df1_day2[' j[mA/cm^2] '].apply(lambda x: f"DAY2 {file1_day2[2]} {file1_day2[1]}%")
df1 = pd.concat([df1_day0,df1_day1,df1_day2])

# REF
file_day0 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY0/REF*.dat',' P[mW/cm^2]')
file_day1 = get_file_by_min_val(f'C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY1/{file_day0[3]}*.dat',' P[mW/cm^2]')
file_day2 = get_file_by_min_val(f'C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY2/{file_day0[3]}*.dat',' P[mW/cm^2]')
df_day0 = pd.read_csv(file_day0[0], delimiter=';')
df_day1 = pd.read_csv(file_day1[0], delimiter=';')
df_day2 = pd.read_csv(file_day2[0], delimiter=';')
df_day0['j']= df_day0[' j[mA/cm^2] '].apply(lambda x: x*-1)
df_day0['Type']= df_day0[' j[mA/cm^2] '].apply(lambda x: f"DAY0 {file_day0[2]} {file_day0[1]}%")
df_day1['j']= df_day1[' j[mA/cm^2] '].apply(lambda x: x*-1)
df_day1['Type']= df_day1[' j[mA/cm^2] '].apply(lambda x: f"DAY1 {file_day1[2]} {file_day1[1]}%")
df_day2['j']= df_day2[' j[mA/cm^2] '].apply(lambda x: x*-1)
df_day2['Type']= df_day2[' j[mA/cm^2] '].apply(lambda x: f"DAY2 {file_day2[2]} {file_day2[1]}%")
df2 = pd.concat([df_day0,df_day1,df_day2])
# V1145
file1_day0 = get_file_by_min_val('C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY0/V1145*.dat',' P[mW/cm^2]')
file1_day1 = get_file_by_min_val(f'C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY1/{file1_day0[3]}*.dat',' P[mW/cm^2]')
file1_day2 = get_file_by_min_val(f'C:/Users/manta/OneDrive/Dokumentai/Python projektai/DATA/DAY2/{file1_day0[3]}*.dat',' P[mW/cm^2]')
df1_day0 = pd.read_csv(file1_day0[0], delimiter=';')
df1_day1 = pd.read_csv(file1_day1[0], delimiter=';')
df1_day2 = pd.read_csv(file1_day2[0], delimiter=';')
df1_day0['j']= df1_day0[' j[mA/cm^2] '].apply(lambda x: x*-1)
df1_day0['Type']= df1_day0[' j[mA/cm^2] '].apply(lambda x: f"DAY0 {file1_day0[2]} {file1_day0[1]}%")
df1_day1['j']= df1_day1[' j[mA/cm^2] '].apply(lambda x: x*-1)
df1_day1['Type']= df1_day1[' j[mA/cm^2] '].apply(lambda x: f"DAY1 {file1_day1[2]} {file1_day1[1]}%")
df1_day2['j']= df1_day2[' j[mA/cm^2] '].apply(lambda x: x*-1)
df1_day2['Type']= df1_day2[' j[mA/cm^2] '].apply(lambda x: f"DAY2 {file1_day2[2]} {file1_day2[1]}%")
df3 = pd.concat([df1_day0,df1_day1,df1_day2])

import seaborn as sns
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2,2,figsize=(15,10))
axes[0,0].set_title(f'REF')
sns.lineplot(data=df[df['U[V] '] >= 0],x = 'U[V] ', y='j', ax=axes[0,0], hue='Type')
axes[1,0].set_title(f'REF by group')
sns.lineplot(data=df2[df2['U[V] '] >= 0],x = 'U[V] ', y='j', ax=axes[1,0], hue='Type')
axes[0,1].set_title(f'V1145')
sns.lineplot(data=df1[df1['U[V] '] >= 0],x = 'U[V] ', y='j', ax=axes[0,1], hue='Type')
axes[1,1].set_title(f'V1145 by group')
sns.lineplot(data=df3[df3['U[V] '] >= 0],x = 'U[V] ', y='j', ax=axes[1,1], hue='Type')
plt.show()