import pandas as pd

# Leo el archivo csv que contiene la tabla de países por población
df = pd.read_csv("paises_por_poblacion.csv")

# Muestro las columnas originales para ver cómo están nombradas
print("Columnas originales:")
for col in df.columns:
    print(repr(col))

# Nombre exacto de la columna de población, sacado de la tabla original
nombre_poblacion = 'Proyección exponencial de la población al 1/7/2025[7]\u200b'

# Renombro las columnas para que tengan nombres más cortos y fáciles de usar
df.rename(columns={
    'País (o territorio dependiente)': 'País',
    nombre_poblacion: 'Población',
    'Total mun- dial (%)': 'Porcentaje_mundial'
}, inplace=True)

# Limpio la columna de población: quito espacios extraños o comas
df["Población"] = df["Población"] \
    .str.replace("\xa0", "", regex=False) \
    .str.replace(" ", "", regex=False) \
    .str.replace(",", "", regex=False)

# Convierto la columna a numérico para poder hacer cálculos
df["Población"] = pd.to_numeric(df["Población"], errors='coerce')

# Ahora limpio la columna del porcentaje mundial (quito símbolos y cambiamos comas por puntos)
df["Porcentaje_mundial"] = df["Porcentaje_mundial"] \
    .str.replace("%", "", regex=False) \
    .str.replace(",", ".", regex=False)

# convierto el porcentaje también a numérico
df["Porcentaje_mundial"] = pd.to_numeric(df["Porcentaje_mundial"], errors='coerce')

# Muestro info general de las columnas para comprobar que están en buen formato
print(df.info())
print(df.head())

# Muestro el top 10 de países con mayor población
top_10 = df.sort_values(by="Población", ascending=False).head(10)
print("Top 10 países por población:")
print(top_10[["País", "Población"]])

# calculo el promedio de población por país (en miles de millones)
promedio_poblacion = df["Población"].mean() / 1_000_000_000
print(f"\nPromedio de población por país: {promedio_poblacion:.2f} mil millones")

# Sumo la población total estimada (en billones)
total_poblacion = df["Población"].sum() / 1_000_000_000_000
print(f"Total población mundial (según tabla): {total_poblacion:.2f} billones")