# Proyecto Tabla Hash

## Enunciado

Realizar una aplicación con interfaz gráfica en Python que:

Para un archivo de texto en disco que contiene 100 registros (descargue en https://app.box.com/s/byiywd1pjrt1p1av9h9ajrz1n2strqb0 ), cada uno con el código de identificación único de 3 dígitos (entre 100 y 999) y el nombre de una persona. El código de identificación, en el archivo en disco, está separado del nombre por una coma. Realizar lo siguiente:

- Generar un índice a través de tablas hash, también en disco (proceso independiente).

- Con dicho índice, el programa debe permitir acceder al nombre de la persona a través de su código de identificación (proceso independiente).

- Listar por pantalla, con base en el índice y ordenación por el método de montículo binario, los nombres (solo mostrar los primeros 10 registros).

- Calcular el número de colisiones que se presentaron para cada tamaño de tabla.
