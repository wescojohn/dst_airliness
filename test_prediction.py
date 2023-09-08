# Division des données en ensembles d'entraînement et de test
X = df_encoded.drop('delayed', axis=1)
y = df_encoded['delayed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Évaluation du modèle
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print(f"RMSE : {rmse}")
print(f"R² : {r2}")

# à rajouter normalement à au fichier flight_delay.py affaire à suivre pour cette partie.