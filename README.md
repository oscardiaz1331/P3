# PAV - P3: estimación de pitch

Esta práctica se distribuye a través del repositorio GitHub [Práctica 3](https://github.com/albino-pav/P3).
Siga las instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para realizar un `fork` de la
misma y distribuir copias locales (_clones_) del mismo a los distintos integrantes del grupo de prácticas.

Recuerde realizar el _pull request_ al repositorio original una vez completada la práctica.

## Ejercicios básicos

- Complete el código de los ficheros necesarios para realizar la estimación de pitch usando el programa
  `get_pitch`.

  - Complete el cálculo de la autocorrelación e inserte a continuación el código correspondiente.

    <img src="im1.png" width="640" align="center">

  - Inserte una gŕafica donde, en un _subplot_, se vea con claridad la señal temporal de un segmento de
    unos 30 ms de un fonema sonoro y su periodo de pitch; y, en otro _subplot_, se vea con claridad la
    autocorrelación de la señal y la posición del primer máximo secundario.

    <img src="rxx.png" width="640" align="center">

  NOTA: es más que probable que tenga que usar Python, Octave/MATLAB u otro programa semejante para
  hacerlo. Se valorará la utilización de la biblioteca matplotlib de Python.

  - Determine el mejor candidato para el periodo de pitch localizando el primer máximo secundario de la
    autocorrelación. Inserte a continuación el código correspondiente.

    <img src="im2.png" width="640" align="center">

  - Implemente la regla de decisión sonoro o sordo e inserte el código correspondiente.

    <img src="im3.png" width="640" align="center">

  - Puede serle útil seguir las instrucciones contenidas en el documento adjunto `código.pdf`.

- Una vez completados los puntos anteriores, dispondrá de una primera versión del estimador de pitch. El
  resto del trabajo consiste, básicamente, en obtener las mejores prestaciones posibles con él.

  - Utilice el programa `wavesurfer` para analizar las condiciones apropiadas para determinar si un
    segmento es sonoro o sordo.

    - Inserte una gráfica con la estimación de pitch incorporada a `wavesurfer` y, junto a ella, los
      principales candidatos para determinar la sonoridad de la voz: el nivel de potencia de la señal
      (r[0]), la autocorrelación normalizada de uno (r1norm = r[1] / r[0]) y el valor de la
      autocorrelación en su máximo secundario (rmaxnorm = r[lag] / r[0]).

      <img src="potrx1rxlag.png" width="640" align="center">

    Puede considerar, también, la conveniencia de usar la tasa de cruces por cero.

    Recuerde configurar los paneles de datos para que el desplazamiento de ventana sea el adecuado, que
    en esta práctica es de 15 ms.

    - Use el estimador de pitch implementado en el programa `wavesurfer` en una señal de prueba y compare
      su resultado con el obtenido por la mejor versión de su propio sistema. Inserte una gráfica
      ilustrativa del resultado de ambos estimadores.

      <img src="wave2.png" width="640" align="center">

    Aunque puede usar el propio Wavesurfer para obtener la representación, se valorará
    el uso de alternativas de mayor calidad (particularmente Python).

  - Optimice los parámetros de su sistema de estimación de pitch e inserte una tabla con las tasas de error
  y el _score_ TOTAL proporcionados por `pitch_evaluate` en la evaluación de la base de datos
  `pitch_db/train`..

    <img src="summary1.png" width="640" align="center">

## Ejercicios de ampliación

- Usando la librería `docopt_cpp`, modifique el fichero `get_pitch.cpp` para incorporar los parámetros del
  estimador a los argumentos de la línea de comandos.

  Esta técnica le resultará especialmente útil para optimizar los parámetros del estimador. Recuerde que
  una parte importante de la evaluación recaerá en el resultado obtenido en la estimación de pitch en la
  base de datos.

  - Inserte un _pantallazo_ en el que se vea el mensaje de ayuda del programa y un ejemplo de utilización
    con los argumentos añadidos.

    <img src="imagenayuda.png" width="640" align="center">

    <img src="imagenayuda2.png" width="640" align="center">

- Implemente las técnicas que considere oportunas para optimizar las prestaciones del sistema de estimación
  de pitch.

  Entre las posibles mejoras, puede escoger una o más de las siguientes:

  - Técnicas de preprocesado: filtrado paso bajo, diezmado, _center clipping_, etc.
    + Usaremos central-clipping, este consiste en declarar un coeficiente, que multiplicado por el valor máximo del tramo que vamos a procesar crea un umbral. Este umbral es comparado con el valor absoulto de la señal y si es menor, se pone a cero esa posición. Haremos este procedimiento dos veces, una para toda la señal global y otra para las tramas individuales.

    <img src="im4.png" width="640" align="center">

    <img src="clip.png" width="640" align="center">
    
  - Técnicas de postprocesado: filtro de mediana, _dynamic time warping_, etc.
    + Usaremos un filtro de mediana de longitud tres. Este filtro consiste en comparar el valor de la muestra actual con el de la muestra anterior y posterior, ordenadorlos en orden ascendente/descendente (no importa), y quedarnos el que este en la posición central (el mediano).

    <img src="im5.png" width="640" align="center">

    <img src="mediana.png" width="640" align="center">

  - Métodos alternativos a la autocorrelación: procesado cepstral, _average magnitude difference function_
    (AMDF), etc.
  - Optimización **demostrable** de los parámetros que gobiernan el estimador, en concreto, de los que
    gobiernan la decisión sonoro/sordo.
  - Cualquier otra técnica que se le pueda ocurrir o encuentre en la literatura.

  Encontrará más información acerca de estas técnicas en las [Transparencias del Curso](https://atenea.upc.edu/pluginfile.php/2908770/mod_resource/content/3/2b_PS%20Techniques.pdf)
  y en [Spoken Language Processing](https://discovery.upc.edu/iii/encore/record/C__Rb1233593?lang=cat).
  También encontrará más información en los anexos del enunciado de esta práctica.

  Incluya, a continuación, una explicación de las técnicas incorporadas al estimador. Se valorará la
  inclusión de gráficas, tablas, código o cualquier otra cosa que ayude a comprender el trabajo realizado.

  - El resultado obtenido aplicando estas dos técnicas es el siguiente:

  <img src="summary2.png" width="640" align="center">

  También se valorará la realización de un estudio de los parámetros involucrados. Por ejemplo, si se opta
  por implementar el filtro de mediana, se valorará el análisis de los resultados obtenidos en función de
  la longitud del filtro.

## Evaluación _ciega_ del estimador

Antes de realizar el _pull request_ debe asegurarse de que su repositorio contiene los ficheros necesarios
para compilar los programas correctamente ejecutando `make release`.

Con los ejecutables construidos de esta manera, los profesores de la asignatura procederán a evaluar el
estimador con la parte de test de la base de datos (desconocida para los alumnos). Una parte importante de
la nota de la práctica recaerá en el resultado de esta evaluación.
