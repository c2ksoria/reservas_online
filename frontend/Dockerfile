FROM node:18-alpine

WORKDIR /app

# Instalar git para clonar y actualizar
RUN apk add --no-cache git

# Clonar el repo si no existe
RUN git clone https://github.com/c2ksoria/reserva_front.git .

# Instalar dependencias
RUN npm install

# Copiar el script de entrada y darle permisos
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh

# Exponer el puerto de desarrollo
EXPOSE 3000

# Ejecutar script personalizado en cada arranque
CMD ["sh", "entrypoint.sh"]