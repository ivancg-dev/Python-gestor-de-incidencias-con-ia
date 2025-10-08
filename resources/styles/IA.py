import os
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# --- Descargar stopwords si no están ---
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
spanish_stopwords = stopwords.words('spanish')

# --- Determinar ruta absoluta del archivo ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'incidencias.txt')

print(f"📄 Intentando leer el archivo desde: {file_path}")

# --- Carga del archivo ---
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
except FileNotFoundError:
    raise FileNotFoundError(f"❌ No se encontró el archivo 'incidencias.txt' en la ruta: {file_path}")

# --- Definir categorías ---
categories = ['leve', 'medio', 'grave', 'extremo']
incidencias = {cat: [] for cat in categories}

# --- Extraer secciones de texto por categoría ---
for category in categories:
    pattern = rf"#\s*Nivel\s+{category}(.*?)(?=#\s*Nivel|$)"
    match = re.search(pattern, data, re.DOTALL | re.IGNORECASE)
    if match:
        lines = [line.strip() for line in match.group(1).split('\n') if line.strip()]
        incidencias[category] = lines
    else:
        print(f"⚠️ Advertencia: No se encontró la sección '# Nivel {category}' en el archivo.")

# --- Crear dataset ---
X = []
y = []

for category in categories:
    for text in incidencias[category]:
        X.append(text)
        y.append(category)

if not X:
    raise ValueError("❌ No se encontraron textos en 'incidencias.txt'. Verifica su formato.")

# --- Vectorización TF-IDF (usa stopwords en español y bigrams) ---
vectorizer = TfidfVectorizer(
    stop_words=spanish_stopwords,
    max_features=3000,
    ngram_range=(1, 2)
)
X_vect = vectorizer.fit_transform(X)

# --- División de datos ---
X_train, X_test, y_train, y_test = train_test_split(
    X_vect, y, test_size=0.2, random_state=42, stratify=y
)

# --- Entrenamiento del modelo ---
model = SVC(kernel='linear', C=1.0, random_state=42)
model.fit(X_train, y_train)

# --- Evaluación ---
y_pred = model.predict(X_test)

print("\n✅ Resultados del modelo:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\n📊 Clasificación detallada:")
print(classification_report(y_test, y_pred, zero_division=0))

# --- Ejemplo de uso ---
text_example = "El ordenador se apaga inesperadamente cuando intento iniciar un programa."
text_vect = vectorizer.transform([text_example])
predicted_category = model.predict(text_vect)[0]

print(f"\n🔍 Predicción para la incidencia:\n'{text_example}' → {predicted_category.upper()}")