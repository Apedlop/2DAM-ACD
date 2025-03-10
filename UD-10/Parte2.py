import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Filtrar datos correctamente
df = pd.read_csv("Barcelona_rent_price.csv", sep=',')

# Filtramos solo los datos correspondientes a 'average rent (euro/month)'
df = df[df['Average _rent'] == 'average rent (euro/month)']
df = df.drop(columns=['Average _rent'])  # Eliminamos la columna 'Average _rent'

# Asegurarse de que 'Year' sea numérico y 'District' sea cadena
df['Year'] = pd.to_datetime(df['Year'], errors='coerce').dt.year
df['District'] = df['District'].astype(str)

# Selección de columnas necesarias
df = df[['Trimester', 'Price', 'District', 'Year']]

# Variables predictoras y objetivo
X = df[['Trimester', 'Year', 'District']]  # Incluimos 'Trimester', 'Year', y 'District'
y = df['Price']  # Objetivo: Precio

# ====================
# ACTIVIDAD 1 - Regresión Lineal
# ====================

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X[['Trimester']], y, test_size=0.2, random_state=42)

# Creamos y ajustamos el modelo de regresión lineal
modelo_lineal = LinearRegression()
modelo_lineal.fit(X[['Trimester']], y)  # Solo usamos 'Trimester' para el modelo lineal

# Predicciones
y_pred = modelo_lineal.predict(X_test)

# Calcular RMSE (Root Mean Squared Error)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # Raíz cuadrada del MSE

print(f'RMSE (Root Mean Squared Error): {rmse:.2f}')

# Tomamos las primeras 20 instancias de X_test
X_test_20 = X_test.head(20)
y_pred_20 = y_pred[:20]  # Predicciones para las 20 instancias

# Visualización de la regresión lineal para 20 instancias
plt.plot(range(20), y_test.head(20), color='blue', marker='o', linestyle='-',  label='Datos reales')  # Puntos originales
plt.plot(range(20), y_pred_20, color='red', marker='x', linestyle='-',  label='Línea de regresión')  # Línea de regresión
plt.title('Regresión Lineal Simple - Precio de Alquiler en Barcelona')
plt.xlabel('Instancias de prueba')
plt.ylabel('Precio (€)')
plt.legend()
plt.grid(True)
plt.show()

# ====================
# ACTIVIDAD 2 - Regresión Lasso
# ====================

# Convertimos las variables categóricas (como 'District') en variables dummy (One-Hot Encoding)
X_dummies = pd.get_dummies(X[['Trimester', 'Year', 'District']], drop_first=True)

# Separar en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_dummies, y, test_size=0.2, random_state=42)

# Escalamos las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_dummies)

# Crear y entrenar el modelo Lasso
lasso = Lasso(alpha=1.0)  # Parámetro de regularización
lasso.fit(X_train, y_train)

# Predicciones usando el modelo Lasso
y_pred_lasso = lasso.predict(X_test)

# Calcular el RMSE (Root Mean Squared Error) para el modelo Lasso
rmse_lasso = np.sqrt(mean_squared_error(y_test, y_pred_lasso))
print(f"RMSE (Root Mean Squared Error) de Lasso: {rmse_lasso:.2f}")

# Visualización de los coeficientes del modelo Lasso
plt.bar(range(X_dummies.shape[1]), lasso.coef_)
plt.xlabel("Índice de las variables predictoras")
plt.ylabel("Valor del coeficiente")
plt.title("Coeficientes en Regresión Lasso")
plt.show()

# Visualización de resultados: Predicciones vs Datos Reales (Primeras 20 instancias)
plt.plot(range(20), y_test[:20], color='blue', marker='o', linestyle='-',  label='Valor Real')  # Valores reales
plt.plot(range(20), y_pred_lasso[:20], marker='x', linestyle='-',  color='red', label='Valor Predicho')  # Predicciones
plt.title('Predicciones vs Datos Reales (Lasso)')
plt.xlabel('Número de Instancia')
plt.ylabel('Valor Predicho')
plt.legend()
plt.grid(True)
plt.show()

# ====================
# ACTIVIDAD 3 - Regresión Random Forest
# ====================

# Convertimos las variables categóricas (como 'District') en variables dummy (One-Hot Encoding)
X_dummies = pd.get_dummies(X[['Trimester', 'Year', 'District']], drop_first=True)

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_dummies, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predicciones
y_pred = rf.predict(X_test)

# Evaluación del modelo
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # Cálculo del RMSE
print(f'RMSE (Root Mean Squared Error): {rmse:.4f}')  # Mostrar el RMSE

# Visualización de resultados: Predicciones vs Datos Reales (Primeras 20 instancias)
plt.plot(range(20), y_test[:20], color='blue', marker='o', linestyle='-', label='Valor Real')  # Valores reales
plt.plot(range(20), y_pred[:20], color='red', marker='x', linestyle='-', label='Valor Predicho')  # Predicciones
plt.title('Predicciones vs Datos Reales (Random Forest)')
plt.xlabel('Número de Instancia')
plt.ylabel('Valor Predicho')
plt.legend()
plt.grid(True)
plt.show()

# ====================
# ACTIVIDAD 4 - Regresión Lineal Simple eliminando Outliers
# ====================

# Utilizamos el rango intercuartílico (IQR) para detectar outliers
Q1 = df['Price'].quantile(0.25)  # Primer cuartil (25%)
Q3 = df['Price'].quantile(0.75)  # Tercer cuartil (75%)
IQR = Q3 - Q1  # Rango intercuartílico

# Definir los límites para detectar outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrar el dataset para eliminar outliers
df_filtered = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]

# Variables predictoras y objetivo (sin outliers)
X_filtered = df_filtered[['Trimester']]  # Usamos solo 'Trimester' como predictor
y_filtered = df_filtered['Price']  # Variable objetivo

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_filtered, y_filtered, test_size=0.2, random_state=42)

# Creamos y ajustamos el modelo de regresión lineal
modelo_lineal_filtered = LinearRegression()
modelo_lineal_filtered.fit(X_train, y_train)  # Solo usamos 'Trimester' para el modelo lineal

# Predicciones
y_pred_filtered = modelo_lineal_filtered.predict(X_test)

# Calcular RMSE (Root Mean Squared Error)
mse_filtered = mean_squared_error(y_test, y_pred_filtered)
rmse_filtered = np.sqrt(mse_filtered)  # Raíz cuadrada del MSE

print(f'RMSE (Root Mean Squared Error) sin outliers: {rmse_filtered:.2f}')

# Tomamos las primeras 20 instancias de X_test
X_test_20 = X_test.head(20)
y_pred_20 = y_pred_filtered[:20]  # Predicciones para las primeras 20 instancias

# Visualización de la regresión lineal para 20 instancias
plt.plot(range(20), y_test.head(20), color='blue', marker='o', linestyle='-', label='Datos reales')  # Puntos originales
plt.plot(range(20), y_pred_20, color='red', marker='x', linestyle='-', label='Línea de regresión')  # Línea de regresión
plt.title('Regresión Lineal Simple - Precio de Alquiler en Barcelona (sin outliers)')
plt.xlabel('Instancias de prueba')
plt.ylabel('Precio (€)')
plt.legend()
plt.grid(True)
plt.show()
