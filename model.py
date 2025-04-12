
import pandas as pd  
import matplotlib.pyplot as plt  
from statsmodels.tsa.api import VAR  
from statsmodels.tsa.stattools import adfuller, grangercausalitytests  

# =============================================================================
# **1. Carga y preparación de datos**  
# =============================================================================
df = pd.read_excel('tasaycambio.xlsx', sheet_name='tasaycambio')  
df['Fecha'] = pd.to_datetime(df['Fecha'])  
df.set_index('Fecha', inplace=True)  

# =============================================================================
# **2. Visualización inicial de las series**  
# =============================================================================
df.plot(subplots=True, figsize=(10, 5), title=['Tasa de Interés Estados Unidos', 'Tipo de Cambio USD GTQ'])  
plt.suptitle('Series originales')  
plt.tight_layout()  
plt.show()  

# =============================================================================
# **3. Prueba de estacionariedad (Dickey-Fuller Aumentado - ADF)**  
#  
# - Evalúa si las series son estacionarias (requisito para modelos VAR).  
# - Hipótesis nula (H0): La serie **no es estacionaria** (tiene raíz unitaria).  
# - Si p-valor < 0.05, se rechaza H0 (la serie es estacionaria).  
# - **Teoría clave**: Series no estacionarias pueden generar regresiones espurias.  
# =============================================================================
def adf_test(series, title=''):  
    result = adfuller(series)  
    print(f'ADF Test para {title}')  
    print(f'  Estadístico: {result[0]}')  
    print(f'  p-valor: {result[1]}')  
    print('  => Estacionaria' if result[1] < 0.05 else '  => NO estacionaria')  
    print()  

adf_test(df['Tasa de Interés USA'], 'Tasa de interés')  
adf_test(df['Tipo de Cambio USD GTQ'], 'Tipo de cambio')  

# =============================================================================
# **4. Transformación a estacionariedad (diferenciación)**  
#  
# - La diferenciación (ΔXₜ = Xₜ − Xₜ₋₁) remueve tendencias.  
# - **Teoría clave**: Integración de orden 1 (I(1)) convierte series no estacionarias en estacionarias.  
# =============================================================================
df_diff = df.diff().dropna()  

# =============================================================================
# **5. Verificación de estacionariedad post-diferenciación**  
#  
# - Confirma que las series transformadas son estacionarias.  
# - **Importante**: Modelos VAR requieren todas las series I(d) con el mismo "d".  
# =============================================================================
print("Verificación después de diferenciar:")  
adf_test(df_diff['Tasa de Interés USA'], 'Tasa de interés (diferenciada)')  
adf_test(df_diff['Tipo de Cambio USD GTQ'], 'Tipo de cambio (diferenciado)')  

# =============================================================================
# **6. Visualización de series diferenciadas**  
#  
# - Grafica las series ya estacionarias para inspección visual.  
# - **Objetivo**: Confirmar que no hay patrones no modelables (ej. heterocedasticidad).  
# =============================================================================
df_diff.plot(subplots=True, figsize=(10, 5), title=['Tasa de Interés USA (Δ)', 'Tipo de Cambio USD GTQ (Δ)'])  
plt.suptitle('Series diferenciadas (estacionarias)')  
plt.tight_layout()  
plt.show()  

# =============================================================================
# **7. Modelado VAR (Vector Autoregression)**  
#  
# - Ajusta un modelo VAR para capturar interdependencias entre series.  
# - `maxlags=4`: Número máximo de rezagos a evaluar.  
# - `ic='aic'`: Selección automática de rezagos óptimos usando el Criterio de Akaike.  
# - **Teoría clave**: VAR modela cada variable como función de sus propios rezagos y los de otras variables.  
# =============================================================================
model = VAR(df_diff)  
results = model.fit(maxlags=4, ic='aic')  
print(results.summary())  

# =============================================================================
# **8. Función de Impulso-Respuesta (IRF)**  
#  
# - Muestra cómo un shock en una variable afecta a otra a lo largo del tiempo.  
# - `irf(10)`: Evalúa efectos durante 10 períodos.  
# - **Teoría clave**: Útil para entender dinámicas de corto/largo plazo entre variables.  
# =============================================================================
irf = results.irf(10)  
irf.plot(orth=False)  
plt.suptitle("Función de Impulso-Respuesta")  
plt.tight_layout()  
plt.show()  

# =============================================================================
# **9. Causalidad de Granger**  
#  
# - Evalúa si una variable ayuda a predecir a otra (no implica causalidad real).  
# - `maxlag=4`: Prueba hasta 4 rezagos.  
# - **Teoría clave**: Si "X Granger-causa Y", los rezagos de X mejoran la predicción de Y.  
# =============================================================================
print("\nTest de Causalidad de Granger:")  
grangercausalitytests(df_diff[['Tipo de Cambio USD GTQ', 'Tasa de Interés USA']], maxlag=4)  

