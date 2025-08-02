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
df = df[df["País"].str.lower() != "mundo"]

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

# Gráfico de barras interactivo con Streamlit
st.subheader("Población por país")

top_30 = df.sort_values(by="Población", ascending=False).head(30).set_index("País")
st.bar_chart(top_30["Población"])

# Gráfico de barras: Top 20 países más poblados
st.subheader("Top 20 países por población")

top_20 = df.sort_values(by="Población", ascending=False).head(20)

fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
ax_bar.barh(top_20["País"], top_20["Población"], color="skyblue")
ax_bar.invert_yaxis()  # País más poblado arriba
ax_bar.set_xlabel("Población")
ax_bar.set_title("Top 20 países por población")
st.pyplot(fig_bar)

# Gráfico de líneas: población acumulada ordenada por país
st.subheader("Población acumulada por país")

# Ordenamos los países por población
ordenados = df.sort_values("Población", ascending=True).reset_index(drop=True)
ordenados["Acumulado"] = ordenados["Población"].cumsum()

fig_line, ax_line = plt.subplots(figsize=(10, 5))
ax_line.plot(ordenados["País"], ordenados["Acumulado"], marker='o', linestyle='-')
ax_line.set_xticks(range(0, len(ordenados), 5))
ax_line.set_xticklabels(ordenados["País"].iloc[::5], rotation=45, ha='right')
ax_line.set_ylabel("Población acumulada")
ax_line.set_title("Población acumulada por país")
st.pyplot(fig_line)

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