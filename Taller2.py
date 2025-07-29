import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo csv (debo asegurarme que esté en la misma carpeta)
df = pd.read_csv("paises_por_poblacion.csv")

# Renombro las columnas para que sea más fácil trabajar con ellas
nombre_poblacion = 'Proyección exponencial de la población al 1/7/2025[7]\u200b'
df.rename(columns={
    'País (o territorio dependiente)': 'País',
    nombre_poblacion: 'Población',
    'Total mun- dial (%)': 'Porcentaje_mundial'
}, inplace=True)

# Limpio la columna "Población" quitando espacios raros y comas
df["Población"] = df["Población"].str.replace("\xa0", "", regex=False).str.replace(" ", "", regex=False).str.replace(",", "", regex=False)

# Convierto los valores a numéricos para poder analizarlos
df["Población"] = pd.to_numeric(df["Población"], errors='coerce')

# Hago lo mismo para "Porcentaje_mundial": limpio símbolos y paso a número
df["Porcentaje_mundial"] = df["Porcentaje_mundial"].str.replace("%", "", regex=False).str.replace(",", ".", regex=False)
df["Porcentaje_mundial"] = pd.to_numeric(df["Porcentaje_mundial"], errors='coerce')

# Agrego un título para la app
st.title("Población mundial por país")

# Calculo y muestro métricas generales usando st.metric
total_poblacion = df["Población"].sum() / 1_000_000_000
promedio_poblacion = df["Población"].mean() / 1_000_000_000
st.metric("Población mundial total (mil millones)", f"{total_poblacion:.2f}")
st.metric("Promedio población por país (mil millones)", f"{promedio_poblacion:.2f}")

# Muestro una tabla con los 10 países más poblados
top_10 = df.sort_values(by="Población", ascending=False).head(10)
st.subheader("Top 10 países por población")
st.dataframe(top_10[["País", "Población"]])

# Creo un gráfico de pastel para visualizar la distribución entre los 10 países
st.subheader("Distribución poblacional de los 10 países más poblados")

fig, ax = plt.subplots()
ax.pie(top_10["Población"], labels=top_10["País"], autopct="%1.1f%%", startangle=90)
ax.axis("equal")  # Esto hace que el gráfico se vea circular
st.pyplot(fig)

# Agrego un selector para que el usuario elija un país y vea sus datos individuales
pais_seleccionado = st.selectbox("Selecciona un país para ver su población y porcentaje mundial", df["País"])

if pais_seleccionado:
    # Muestro los datos del país seleccionado
    info = df[df["País"] == pais_seleccionado][["Población", "Porcentaje_mundial"]].iloc[0]
    st.write(f"**Población:** {int(info['Población']):,}")
    st.write(f"**Porcentaje mundial:** {info['Porcentaje_mundial']:.2f}%")

#Al fin me puedo ir a descansar señor Stark.