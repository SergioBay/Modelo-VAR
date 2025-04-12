<h1 align="center">Desarrollo de Modelo VAR</h1>
La resolución del modelo se hizo a través del lenguaje de programación Python, utilizando las librerías: 

- pandas: para la lectura de la base de datos almacenada en Excel. 
- matplotlib: para la representación de gráficos. 
- statsmodels: permitió la elaboración de modelos estadísticos. 

Los resultados del la prueba se presentan a continuación. 


<h3 align="left">Grafico Tasa de interés Estados Unidos y Tipo de Cambio USD/GTQ</h3>

<p align="center">
  <img alt="Alacritty - A fast, cross-platform, OpenGL terminal emulator"
       src="Tasa de interes-Tipo de cambio.png">
</p>
<h3 align="left">Resultados del Test de Estacionariedad (ADF)</h3>

| Variable               | Estadístico ADF | p-valor   | Conclusión         |
|------------------------|------------------|-----------|---------------------|
| Tasa de interés        | -0.3001          | 0.9255    | NO estacionaria     |
| Tipo de cambio USD/GTQ | -1.5496          | 0.5089    | NO estacionaria     |

Los resultados de la prueba Dickey-Fuller Aumentado (ADF) muestran los siguientes resultados. 

En la tasa de interés se indica que no se puede rechazar la hipótesis nula de no estacionariedad.

El tipo de cambio presentó valores muy por encima del umbral de significancia típico de 0.05. Esto confirma que ambas series presentan tendencias u otras formas de no estacionariedad, por lo que no son adecuadas para el modelado VAR en su forma original. 

En consecuencia, fue necesario aplicar una transformación mediante diferenciación para eliminar estas tendencias y asegurar que las series sean estacionarias antes de continuar con el análisis. 


| Variable                            | Estadístico ADF | p-valor | Conclusión    |
|-------------------------------------|------------------|---------|----------------|
| Tasa de interés (diferenciada)      | -61.8965         | 0.0000  | Estacionaria   |
| Tipo de cambio USD/GTQ (diferenciado)| -20.3623         | 0.0000  | Estacionaria   |


<p align="center">
  <img alt="Alacritty - A fast, cross-platform, OpenGL terminal emulator"
       src="Series Diferenciadas.png">
</p>

<h3 align="left">Resultados en Python de la aplicación del Modelo VAR<h3>


### Información del Modelo
| Métrico               | Valor               |
|-----------------------|---------------------|
| Modelo                | VAR                 |
| Método                | MCO                 |
| Fecha                 | Vie, 11 Abr 2025    |
| Hora                  | 20:22:36            |
| N° de Ecuaciones      | 2                   |
| Nobs                  | 3649                |
| Log Likelihood        | 20141.4             |
| AIC                   | -16.7053            |
| BIC                   | -16.6747            |
| HQIC                  | -16.6944            |
| FPE                   | 5.55885e-08         |
| Det(Omega_mle)        | 5.53153e-08         |

---

### Ecuación 1: Tasa de Interés EE.UU.
| Rezago | Variable                | Coeficiente | Error Estándar | t-estadístico | p-valor |
|--------|-------------------------|-------------|----------------|---------------|---------|
| -      | const                   | 0.001205    | 0.000659       | 1.827         | 0.068   |
| L1     | Tasa de Interés EE.UU.  | -0.024862   | 0.016578       | -1.500        | 0.134   |
| L1     | Tipo de Cambio USD GTQ  | 0.177019    | 0.110970       | 1.595         | 0.111   |
| L2     | Tasa de Interés EE.UU.  | -0.005016   | 0.016579       | -0.303        | 0.762   |
| L2     | Tipo de Cambio USD GTQ  | -0.052731   | 0.112447       | -0.469        | 0.639   |
| L3     | Tasa de Interés EE.UU.  | -0.013848   | 0.016579       | -0.835        | 0.404   |
| L3     | Tipo de Cambio USD GTQ  | -0.116591   | 0.112450       | -1.037        | 0.300   |
| L4     | Tasa de Interés EE.UU.  | -0.001542   | 0.016572       | -0.093        | 0.926   |
| L4     | Tipo de Cambio USD GTQ  | 0.063169    | 0.111030       | 0.569         | 0.569   |

---

### Ecuación 2: Tipo de Cambio USD GTQ
| Rezago | Variable                | Coeficiente | Error Estándar | t-estadístico | p-valor |
|--------|-------------------------|-------------|----------------|---------------|---------|
| -      | const                   | 0.000022    | 0.000098       | 0.224         | 0.823   |
| L1     | Tasa de Interés EE.UU.  | -0.000565   | 0.002467       | -0.229        | 0.819   |
| L1     | Tipo de Cambio USD GTQ  | 0.162171    | 0.016511       | 9.822         | <0.001  |
| L2     | Tasa de Interés EE.UU.  | 0.001593    | 0.002467       | 0.646         | 0.518   |
| L2     | Tipo de Cambio USD GTQ  | -0.061820   | 0.016731       | -3.695        | <0.001  |
| L3     | Tasa de Interés EE.UU.  | -0.000271   | 0.002467       | -0.110        | 0.913   |
| L3     | Tipo de Cambio USD GTQ  | 0.015159    | 0.016731       | 0.906         | 0.365   |
| L4     | Tasa de Interés EE.UU.  | -0.006702   | 0.002466       | -2.718        | 0.007   |
| L4     | Tipo de Cambio USD GTQ  | 0.079876    | 0.016520       | 4.835         | <0.001  |

---

### Matriz de Correlación de Residuales
|                          | Tasa de Interés EE.UU. | Tipo de Cambio USD GTQ |
|--------------------------|-----------------------|------------------------|
| Tasa de Interés EE.UU.   | 1.000000              | 0.020765               |
| Tipo de Cambio USD GTQ    | 0.020765              | 1.000000               |

<h3 align="left">Resultados de Función Impulso - Respuesta<h3>
<p align="center">
  <img alt="Alacritty - A fast, cross-platform, OpenGL terminal emulator"
       src="Función Impulso Respuesta.png">
</p>

<h3 align="left">Resultados de Test de Causalidad de Granger<h3>

### Niveles de Rezago Analizados:

#### Rezago 1:
| Prueba                  | Estadístico | p-valor | Grados de Libertad |
|-------------------------|-------------|---------|--------------------|
| SSR-based F-test        | F = 0.1502  | 0.6983  | (1, 3649)          |
| SSR-based χ²-test       | χ² = 0.1504 | 0.6982  | 1                  |
| Likelihood ratio test   | χ² = 0.1504 | 0.6982  | 1                  |
| Parameter F-test        | F = 0.1502  | 0.6983  | (1, 3649)          |

---

#### Rezago 2:
| Prueba                  | Estadístico | p-valor | Grados de Libertad |
|-------------------------|-------------|---------|--------------------|
| SSR-based F-test        | F = 0.2552  | 0.7748  | (2, 3646)          |
| SSR-based χ²-test       | χ² = 0.5112 | 0.7745  | 2                  |
| Likelihood ratio test   | χ² = 0.5111 | 0.7745  | 2                  |
| Parameter F-test        | F = 0.2552  | 0.7748  | (2, 3646)          |


---

#### Rezago 3:
| Prueba                  | Estadístico | p-valor | Grados de Libertad |
|-------------------------|-------------|---------|--------------------|
| SSR-based F-test        | F = 0.1523  | 0.9282  | (3, 3643)          |
| SSR-based χ²-test       | χ² = 0.4578 | 0.9281  | 3                  |
| Likelihood ratio test   | χ² = 0.4578 | 0.9281  | 3                  |
| Parameter F-test        | F = 0.1523  | 0.9282  | (3, 3643)          |


---

#### Rezago 4:
| Prueba                  | Estadístico | p-valor | Grados de Libertad |
|-------------------------|-------------|---------|--------------------|
| SSR-based F-test        | F = 1.9679  | 0.0966  | (4, 3640)          |
| SSR-based χ²-test       | χ² = 7.8909 | 0.0957  | 4                  |
| Likelihood ratio test   | χ² = 7.8824 | 0.0960  | 4                  |
| Parameter F-test        | F = 1.9679  | 0.0966  | (4, 3640)          |

---

Aclaración: algunos campos en las tablas fueron traducidos a español. Por defecto, los resultados se muestran en inglés. 