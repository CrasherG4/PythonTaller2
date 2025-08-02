import requests
from bs4 import BeautifulSoup
import pandas as pd

# url de la página que contiene la tabla de países por población
url = "https://es.wikipedia.org/wiki/Anexo:Países_por_población"

# Cro un encabezado para que el servidor no bloquee nuestra solicitud (como si imitasemos un navegador vaya)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Hago la solicitud get para obtener el contenido de la página
response = requests.get(url, headers=headers)

# Verifico que la página haya respondido correctamente el codigo 200 me indica que está correcto
if response.status_code == 200:
    # Uso BeautifulSoup para analizar el html de la página
    soup = BeautifulSoup(response.text, "html.parser")

    # Busco la primera tabla con clase wikitable, que es la que contiene los datos
    table = soup.find("table", {"class": "wikitable"})

    # Uso pandas para leer el contenido de la tabla directamente desde el html
    df = pd.read_html(str(table))[0]

    # Guardo los datos extraídos en un archivo csv
    df.to_csv("paises_por_poblacion.csv", index=False, encoding="utf-8")

    # Muestro un mensaje para confirmar que todo salió bien
    print("Datos extraídos y guardados en un archivo llamado paises_por_poblacion.csv")

else:
    # Si hubo un problema al acceder a la página, muestro un mensaje de error
    print(f"Error al acceder a la página.")
    
# Esto parece que lo escribió una IA xd me van a poner 0.