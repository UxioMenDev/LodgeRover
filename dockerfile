FROM python:3.12.8

# Establecer el directorio de trabajo
WORKDIR /

# Copiar los archivos de requisitos y el código fuente
COPY /authenticate /authenticate/
COPY /customer /customer/
COPY /payment /payment/
COPY /reservation /reservation/
COPY /reservation_app /reservation_app/
COPY /room /room/
COPY /media /media
COPY manage.py /
COPY requirements.txt /


# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt


# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENV PYTHONUNBUFFERED=1