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

# Creamos y ajustamos el modelo de regresión lineal
modelo_lineal = LinearRegression()
modelo_lineal.fit(X[['Trimester']], y)  # Solo usamos 'Trimester' para el modelo lineal

# Predicciones
y_pred = modelo_lineal.predict(X[['Trimester']])

# Calcular RMSE (Root Mean Squared Error)
mse = mean_squared_error(y, y_pred)  # Error cuadrático medio
rmse = np.sqrt(mse)  # Raíz cuadrada del MSE

print(f'RMSE (Root Mean Squared Error): {rmse:.2f}')
print("Intercepto (w₀):", modelo_lineal.intercept_)
print("Pendiente (w₁):", modelo_lineal.coef_[0])

# Visualización de la regresión lineal
plt.scatter(X[['Trimester']], y, color='blue', label='Datos')  # Puntos originales
plt.plot(X[['Trimester']], y_pred, color='red', label='Línea de regresión')  # Línea de regresión
plt.title('Regresión Lineal Simple - Precio de Alquiler en Barcelona')
plt.xlabel('Trimestre')
plt.ylabel('Precio (€)')
plt.legend()
plt.grid(True)
plt.show()

# ====================
# ACTIVIDAD 2 - Regresión Lasso
# ====================

# Convertimos las variables categóricas (como 'District') en variables dummy (One-Hot Encoding)
X_dummies = pd.get_dummies(X[['Trimester', 'Year', 'District']], drop_first=True)

# Escalamos las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_dummies)

# Separar en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo Lasso
lasso = Lasso(alpha=1.0)  # Parámetro de regularización
lasso.fit(X_train, y_train)

# Mostrar coeficientes del modelo Lasso
print("Coeficientes del modelo Lasso:", lasso.coef_)

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

# Visualización de resultados: Predicciones vs Datos Reales
plt.scatter(y_test, y_pred_lasso, color='blue', label='Datos Reales vs Predicción')  # Puntos de predicción vs reales
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Línea Perfecta')  # Línea ideal
plt.title('Predicciones vs Datos Reales (Lasso)')
plt.xlabel('Valor Real')
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
# Evaluación del modelo
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # Cálculo del RMSE
print(f'Error Cuadrático Medio (MSE): {mse:.4f}')
print(f'Root Mean Squared Error (RMSE): {rmse:.4f}')  # Mostrar el RMSE

# Visualización de la regresión
# Creamos un grid para la variable 'Trimester' para la visualización (suponiendo que se necesita para una visualización continua)
X_grid = np.linspace(X['Trimester'].min(), X['Trimester'].max(), 100).reshape(-1, 1)

# Para la predicción, tenemos que replicar la estructura de las variables dummy como en el entrenamiento
X_grid_df = pd.DataFrame({'Trimester': X_grid.flatten(), 'Year': np.repeat(2025, 100), 'District': np.repeat('Central', 100)})
X_grid_dummies = pd.get_dummies(X_grid_df, drop_first=True)

# Asegurarnos de que las columnas coincidan entre entrenamiento y predicción
X_train_columns = X_train.columns
X_grid_dummies = X_grid_dummies.reindex(columns=X_train_columns, fill_value=0)

y_grid_pred = rf.predict(X_grid_dummies)

# Visualización
plt.scatter(X['Trimester'], y, color='blue', label='Datos originales')
plt.plot(X_grid, y_grid_pred, color='red', label='Predicción Random Forest')
plt.title('Regresión con Random Forest - Precio de Alquiler en Barcelona')
plt.xlabel('Trimester')
plt.ylabel('Precio (€)')
plt.legend()
plt.show()

# ====================
# ACTIVIDAD 4 - Regresión Lineal Simple eliminando Outliers
# ====================

# Paso 1: Identificar y eliminar outliers en la variable objetivo (Price)
# Utilizamos el rango intercuartílico (IQR) para detectar outliers
Q1 = df['Price'].quantile(0.25)  # Primer cuartil (25%)
Q3 = df['Price'].quantile(0.75)  # Tercer cuartil (75%)
IQR = Q3 - Q1  # Rango intercuartílico

# Definir los límites para detectar outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrar el dataset para eliminar outliers
df_filtered = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]

# Paso 2: Ajustar un modelo de regresión lineal simple
# Variables predictoras y objetivo (sin outliers)
X_filtered = df_filtered[['Trimester']]  # Usamos solo 'Trimester' como predictor
y_filtered = df_filtered['Price']  # Variable objetivo

# Crear y ajustar el modelo de regresión lineal
modelo_lineal_filtered = LinearRegression()
modelo_lineal_filtered.fit(X_filtered, y_filtered)

# Predicciones
y_pred_filtered = modelo_lineal_filtered.predict(X_filtered)

# Paso 3: Evaluar el modelo
# Calcular RMSE (Root Mean Squared Error)
mse_filtered = mean_squared_error(y_filtered, y_pred_filtered)  # Error cuadrático medio
rmse_filtered = np.sqrt(mse_filtered)  # Raíz cuadrada del MSE

print(f'RMSE (Root Mean Squared Error) sin outliers: {rmse_filtered:.2f}')
print("Intercepto (w₀) sin outliers:", modelo_lineal_filtered.intercept_)
print("Pendiente (w₁) sin outliers:", modelo_lineal_filtered.coef_[0])

# Visualización de la regresión lineal sin outliers
plt.scatter(X_filtered, y_filtered, color='blue', label='Datos sin outliers')  # Puntos originales sin outliers
plt.plot(X_filtered, y_pred_filtered, color='red', label='Línea de regresión')  # Línea de regresión
plt.title('Regresión Lineal Simple - Precio de Alquiler en Barcelona (sin outliers)')
plt.xlabel('Trimestre')
plt.ylabel('Precio (€)')
plt.legend()
plt.grid(True)
plt.show()

# Comparación de resultados con y sin outliers
print("\nComparación de resultados:")
print(f"RMSE con outliers: {rmse:.2f}")
print(f"RMSE sin outliers: {rmse_filtered:.2f}")