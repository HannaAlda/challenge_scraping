FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
