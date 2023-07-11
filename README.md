# api-tp-final

Para crear la imagen del el servidor de la api

sudo docker build -t serverapi .

Para levantar el contenedor con la imagen anterior y exponerlo en el puerto 8000

sudo docker run -itd --rm -p 8000:8000 --name serverdev serverapi
