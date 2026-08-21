2) Punto 2, Trabajo Practico 1

**A) Tipo y modo de transmision:**

        El esquema muestra dos "Modulos de comunicacion" conectados por dos lineas: una de ellas es de datos y otra de reloj donde cada modulo tiene
    su propio reloj sincronizado, y las flechas van en un solo sentido (izquierda a derecha). 
        # La direccionalidad es de modo simplex, es decir, los datos viajan en una sola doreccion.
        # Sus caracteristicas temporales son sincronica debido a que hay una senial de reloj compartida entre ambos modulos que marcan cuando leer cada bit.
        # Un detalle a mencionar es que es seria (serial), es decir, que los bits se transmiten uno detras de otro por una unica linea de datos, no
        es en paralelo.

**B) Es este el mejor paradigma si busco transmitir datos rapidamente y de forma bidireccional?**

        No, este esquema no permite la bidireccionalidad porque es de esquema simplex. Para lograr mayor velocidad y comunicacion de datos en ambos sentidos, necesitariamos minimamente Half-Duplex (ambos sentidos pero no simultaneos) o Full-Duplex (ambos sentidos simultaneos)

**C) Transmitir la 4ta letra del nombre del grupo**

    La cuarta letra del nombre del grupo es a, en ASCII es 97 y en binario es 01100001

    Diagrama:
![Diagrama](image-1.png)   

**D) Donde medir la senial? Dada la pendiente**

        Como la transicion de tension no es instantanea (visualizadas con las flechas rojas), no conviene medir justo en el borde/flacon de subida
    bajada porque ahi el valor esta en transicion y podria tener una lectura erronea.
        Lo correcto seria medir en el punto medio del intervalo de cada bit. dando tiempo a que la senial suba o baje antes del muestreo.
