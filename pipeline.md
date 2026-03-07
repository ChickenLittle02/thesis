Para fichas de catálogo antiguas como las que mostraste (tarjetas bibliográficas mecanografiadas), se puede diseñar un **pipeline especializado** que aprovecha dos cosas clave:

* **estructura visual muy estable**
* **patrones bibliográficos repetitivos**

Con eso se puede lograr **≈90–95 % de precisión** sin intervención humana en la mayoría de los casos.

A continuación te doy **un algoritmo específico + el pipeline completo**.

---

# 1️⃣ Pipeline completo para fichas catalográficas

```
Escaneo / Imagen
      │
      ▼
Preprocesamiento de imagen
(OpenCV)
      │
      ▼
OCR estructurado
(Tesseract hOCR)
      │
      ▼
Segmentación de zonas de la ficha
(Layout detection)
      │
      ▼
Clasificación de líneas por reglas bibliográficas
      │
      ▼
Normalización semántica
(heurísticas o LLM)
      │
      ▼
Conversión automática a MARC21
      │
      ▼
Validación bibliográfica
```

---

# 2️⃣ Paso 1 — Preprocesamiento de imagen

Esto mejora muchísimo el OCR.

Procesos:

* binarización adaptativa
* corrección de inclinación
* eliminación de ruido
* aumento de contraste

Ejemplo con **OpenCV**:

```python
import cv2

img = cv2.imread("ficha.jpg", 0)

# binarización
thresh = cv2.adaptiveThreshold(
    img,255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,2
)

# deskew (corrección inclinación)
coords = cv2.findNonZero(thresh)
angle = cv2.minAreaRect(coords)[-1]

if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle

(h,w) = thresh.shape
M = cv2.getRotationMatrix2D((w//2,h//2), angle, 1)
deskew = cv2.warpAffine(thresh,M,(w,h))
```

---

# 3️⃣ Paso 2 — OCR estructurado

Usar **OCR con coordenadas**, no texto plano.

Con **Tesseract OCR**:

```python
import pytesseract
from pytesseract import Output

data = pytesseract.image_to_data(
    deskew,
    lang="spa",
    output_type=Output.DATAFRAME
)
```

Esto devuelve:

| palabra | x | y | línea |
| ------- | - | - | ----- |

---

# 4️⃣ Paso 3 — Segmentación de zonas

Las fichas antiguas casi siempre tienen **4 zonas**:

```
┌─────────────────────────────┐
│ Clasificación                │
│ (arriba izquierda)           │
├─────────────────────────────┤
│ Autor / Institución          │
│ Título                       │
├─────────────────────────────┤
│ Publicación                  │
│ Descripción física           │
├─────────────────────────────┤
│ Serie / notas                │
└─────────────────────────────┘
```

Algoritmo simple:

```
si y < 80 → zona_clasificacion
si 80 < y < 180 → zona_autor_titulo
si 180 < y < 280 → zona_publicacion
si y > 280 → zona_notas
```

---

# 5️⃣ Paso 4 — Clasificación de líneas

Aquí se identifica cada campo bibliográfico.

## Clasificación

Patrón:

```
^\d{3}
```

Ejemplo:

```
997
```

---

## Autor

Patrones:

* institución
* apellido + coma

Regex:

```
^[A-ZÁÉÍÓÚÑ].+, 
```

o palabras clave:

```
Academia
Universidad
Instituto
Ministerio
```

---

## Título

Normalmente:

* línea más larga
* aparece después del autor

Heurística:

```
linea_longitud > 30 caracteres
```

---

## Publicación

Patrón típico:

```
Ciudad, Editorial, Año
```

Regex:

```
.*, \d{4}
```

Ejemplo:

```
Moscú, Ciencias Sociales Contemporáneas, 1983
```

---

## Descripción física

Patrones:

```
p.
cm
ilus.
```

Regex:

```
\d+\s*p\.
```

Ejemplo:

```
166 p. 22 cm
```

---

## Serie

Las series casi siempre están **entre paréntesis**:

```
\(.*\)
```

Ejemplo:

```
(Problemas del mundo contemporáneo; 100)
```

---

## Nota bibliográfica

Palabras clave:

```
bibliografía
incluye
bibliografia
```

---

# 6️⃣ Paso 5 — Construcción del registro MARC

Ejemplo:

```json
{
 "082": "997",
 "110": "Academia de Ciencias de la URSS",
 "245": "La crisis de las Malvinas (Falkland): orígenes y consecuencias",
 "260": "Moscú : Ciencias Sociales Contemporáneas, 1983",
 "300": "166 p. ; 22 cm",
 "490": "América Latina: estudios de científicos soviéticos ; 2",
 "504": "Incluye bibliografía"
}
```

Formato bibliográfico estándar:

**MARC 21**

---

# 7️⃣ Paso 6 — Validación automática

Reglas útiles:

### año válido

```
1900–2025
```

### páginas

```
\d+ p
```

### tamaño

```
\d+ cm
```

---

# 8️⃣ Algoritmo completo simplificado

```
function procesar_ficha(imagen):

    imagen = preprocess(imagen)

    texto_ocr = tesseract(imagen)

    lineas = agrupar_lineas(texto_ocr)

    zonas = segmentar_por_coordenadas(lineas)

    clasificacion = detectar_clasificacion(zonas)

    autor = detectar_autor(zonas)

    titulo = detectar_titulo(zonas)

    publicacion = detectar_publicacion(zonas)

    descripcion = detectar_descripcion(zonas)

    serie = detectar_serie(zonas)

    notas = detectar_notas(zonas)

    registro = convertir_a_MARC(
        clasificacion,
        autor,
        titulo,
        publicacion,
        descripcion,
        serie,
        notas
    )

    return registro
```

---

# 9️⃣ Precisión real que se obtiene

En proyectos de digitalización de catálogos de fichas:

| método                | precisión   |
| --------------------- | ----------- |
| OCR simple            | 60–70 %     |
| OCR + regex           | 80 %        |
| OCR + layout + reglas | **90–95 %** |

Esto funciona bien porque **las fichas catalográficas son extremadamente uniformes**.

---
