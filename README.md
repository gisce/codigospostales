# Códigos postales con código INE

## Fuente de datos

- [Callejero del Censo Electoral](https://www.ine.es/uc/1dIJtjmEi1) (INE)
- [Nomenclator](https://www.ine.es/uc/d3JnUsAO) (INE)

## Preparación ficheros

### Callejero del Censo Electoral

Del fichero zip del callejero nos interesa el fichero `TRAM.XXXX`

> [!WARNING]
El problema es que el nombre del pueblo está limitado a 25 carácteres con lo que no tenemos todos los nombres correctos... para eso utilizaremos el **Nomenclator** y *mezclaremos* los dos ficheros

### Nomenclator para corregir el nombre de la población

Del fichero del Nomenclator nos interesa el fichero `NomdefXXX.txt`

## Mezcla de ficheros

Construcción fichero final:

- Si no tenemos pandas lo debemos instalar:

```bash
pip install pandas
```
- Creamos el fichero `zipcodes.csv`

```bash
python merge.py <tram_path> <nomdef_path> <output_path>
```

Donde:
- `<tram_path>` es la ruta al fichero `tramos.txt` (preparado a partir del Callejero del Censo Electoral).
- `<nomdef_path>` es la ruta al fichero `pobs.txt` (preparado a partir del Nomenclator).
- `<output_path>` es la ruta donde se guardará el fichero `zipcodes.csv` resultante.
