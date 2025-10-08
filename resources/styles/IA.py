import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

with open('incidencias.txt', 'r', encoding='utf-8') as file:
    data = file.read()
categories = ['leve', 'medio', 'grave', 'extremo']
incidencias = {'leve': [], 'medio': [], 'grave': [], 'extremo': []}

for category in categories:
    section = data.split(f'# nivel {category}')[1]
    section = section.split(f'# nivel')[0]
    incidencias[category] = section.split('\n')

X = []
y = []

for category in categories:
    for text in incidencias[category]:
        X.append(text.strip())
        y.append(category)

vectorizer = TfidfVectorizer(stop_words='english')
X_vect = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

model = SVC(kernel='linear')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClasificación detallada:")
print(classification_report(y_test, y_pred))

#ejemplo de uso
text_example = "El ordenador se apaga inesperadamente cuando intento iniciar un programa."
text_vect = vectorizer.transform([text_example])
predicted_category = model.predict(text_vect)
print(f"Predicción para la incidencia: '{text_example}' -> {predicted_category[0]}")