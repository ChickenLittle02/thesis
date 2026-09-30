En esta máquina **ya puedes compilar en local**. Tienes `pdflatex`, `latexmk`, LaTeX Workshop y visores de PDF. No hace falta subir a GitHub para ver el resultado.

## Opción más simple: terminal

Desde la carpeta del manuscrito:

```bash
cd /home/nebur02/Documents/TESIS/Repos/thesis/document
latexmk
```

Eso genera `document/Thesis.pdf`. Para abrirlo:

```bash
xdg-open Thesis.pdf
```

`latexmk` usa el `latexmkrc` de la plantilla: compila `Thesis.tex` con `pdflatex` las veces que hagan falta (referencias, índice, bibliografía).

Otros comandos útiles:

```bash
latexmk -pvc     # recompila solo al guardar
latexmk -c       # borra auxiliares (.aux, .log, …) y deja el PDF
```

## Opción cómoda: Cursor / VS Code

1. Instala/activa la extensión **LaTeX Workshop** (ya la tienes: `james-yu.latex-workshop`).
2. Abre **`document/Thesis.tex`** (el archivo raíz, no un capítulo suelto).
3. Compila con `Ctrl+Alt+B`, o guarda si tienes *build on save*.
4. Vista previa: `Ctrl+Alt+V`, o el icono de PDF en la barra de LaTeX Workshop.

Puedes editar `MainMatter/Introduction.tex` y el resto de capítulos; al compilar el raíz, LaTeX mete todos los `\include{...}`.

## Cómo ver el PDF

En el explorador de archivos del editor el PDF **está oculto** a propósito (la plantilla esconde `*.pdf` para no llenar el árbol de auxiliares). Eso no impide la vista previa de LaTeX Workshop ni Abrir con Evince/Okular.

Si quieres ver `Thesis.pdf` en el árbol, en `.vscode/settings.json` se puede dejar de ocultar ese archivo.

## Flujo de trabajo recomendado

1. Editas, por ejemplo, `document/MainMatter/Introduction.tex`.
2. Compilas en local y revisas el PDF.
3. Cuando te convenza, haces commit y push.
4. GitHub Actions vuelve a compilar lo mismo, pero en la nube.

Local y GitHub usan la misma raíz: `document/Thesis.tex`.

## Un detalle de bibliografía

Tienes `biblatex`, pero **no está instalado `biber`**. El PDF ya se genera; las citas de `Bibliography.bib` pueden no actualizarse bien. Si al citar ves `?` o la bibliografía no sale:

```bash
sudo apt install biber
```

Luego, otra vez `latexmk` dentro de `document/`.