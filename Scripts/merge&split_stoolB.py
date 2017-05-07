import glob
import pandas as pd


# Fichero auxiliar con el nombre de los ficheros a añadir
sup_f = open("StoolB_samples.txt","r")
sup_f_text = sup_f.read().split("\n")
sup_f.close()

# Generar lista de tablas por día
list_of_dic = []
for i in sup_f_text:
    try:
        # Ficheros de abundancia absoluta:
        file = "absolute_L6_" + i
        f_in = open(file, "r")
        text = f_in.read()
        f_in.close()
        
        # Quitar cabecera
        sentences = text.split("\n")
        sentences = "\t".join(sentences)
        sentences = sentences.split("\t")
        
        sample = sentences[2]
        sentences = sentences[3:]
        
        # Crear un diccionario que sirve como tabla final
        otu = []
        abundance = []
        
        for j in range(len(sentences)):
            if j%2 == 0:
                otu.append(sentences[j])
            else:
                abundance.append(float(sentences[j]))
            
        raw_data = {
                "otu_id": otu,
                sample: abundance} 
        
        df_a = pd.DataFrame(raw_data, columns = ["otu_id", sample])
        list_of_dic.append(df_a)
    except:
        print("No se encuentra el fichero" + str(i))

# Crear una tabla única final
f_table = list_of_dic[0]

for k in range(1, len(list_of_dic)):
    f_table = pd.merge(f_table, list_of_dic[k], on="otu_id", how="outer")


# Dividir tabla final en intervalos de tiempo y guardar cada subtabla en una hoja excel
df2 = f_table.iloc[:,1:25]
df2.insert(0, "otu_id",value=f_table.iloc[:,0])
df3 = f_table.iloc[:,25:83]
df3.insert(0, "otu_id",value=f_table.iloc[:,0])
df4 = f_table.iloc[:,83:115]
df4.insert(0, "otu_id",value=f_table.iloc[:,0])
df5 = f_table.iloc[:,115:131]
df5.insert(0, "otu_id",value=f_table.iloc[:,0])
df6 = f_table.iloc[:,131:187]
df6.insert(0, "otu_id",value=f_table.iloc[:,0])

# Formatear salida
pd.set_option("expand_frame_repr", False)

# Escribir cada dataframe en una hoja Excel diferente
writer = pd.ExcelWriter("HostLifeStyle_StoolB_absolute.xlsx")
f_table.to_excel(writer, sheet_name="StoolB", index = True, na_rep = 0)
df2.to_excel(writer, sheet_name="h_StoolB_Day0to24",index = False, na_rep = 0)
df3.to_excel(writer, sheet_name="h_StoolB_Day25to99",index = False, na_rep = 0)
df4.to_excel(writer, sheet_name="h_StoolB_Day100to142",index = False, na_rep = 0)
df5.to_excel(writer, sheet_name="StoolB_Day143to162_infection",index = False, na_rep = 0)
df6.to_excel(writer, sheet_name="StoolB_Day163to318_hypothesis_h",index = False, na_rep = 0)

# Cerrar el escritor Pandas Excel y guardar el fichero
writer.save()