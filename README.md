# Códigos postales con código INE

## Fuente de datos

- [Callejero del Censo Electoral](http://www.ine.es/ss/Satellite?L=es_ES&c=Page&cid=1254735624326&p=1254735624326&pagename=ProductosYServicios%2FPYSLayout) (INE)
- [Nomenclator](
http://www.ine.es/nomen2/ficheros.do) (INE)

## Preparación ficheros

### Callejero del Censo Electoral

Del callejero censal nos interesa el fichero `TRAMOS_NAL.zip` que dentro habrá otro fichero `TRAMOS-NAL.F181231`

- Pasamos a codificación **UTF-8**
```
$ iconv TRAMOS-NAL.F181231 --from=iso-8859-1 --to=utf-8 > tramos.txt
```
- Cogemos los campos: código INE, Código Postal, Código unidad poblacional (resumido), Nombre del población
```
$ cat tramos.txt | cut -c 1-5,43-47,79-82,111-135 --output-delimiter=';' | sort | uniq | grep -v 'DISEMINADO' > cps.txt
```

Nos debería quedar un fichero similar a:
```
01001;01193;0002;EGILETA                  
01001;01240;0001;ALEGRIA-DULANTZI         
01002;01450;0005;BARANBIO                 
01002;01450;0008;LEKAMAÑA                
01002;01450;0009;LEZAMA                   
01002;01468;0001;ALORIA                   
01002;01468;0003;ARTOMAÑA 
```

:warning: El problema es que el nombre del pueblo está limitado a 25 carácteres con lo que no tenemos todos los nombres correctos... para eso utilizaremos el **Nomenclator** y *mezclaremos* los dos ficheros

### Nomenclator para corregir el nombre de la población

- Corregimos codificación a **UTF-8**

```
$ iconv Nomdef2018.txt --from=iso-8859-1 --to=utf-8 > nomenclator.txt
```

- Cogemos los campos que nos interessan: Código INE, Unidad poblacional (resumido), Nombre población

```
$ cat nomenclator.txt | cut -c 1-5,6-9,12-81 --output-delimiter=';' | grep -v 'DISEMINADO' > pobs.txt
```

Debería quedar un fichero similar a 

```
01001;0000;ALEGRÍA-DULANTZI                                                     
01001;0001;ALEGRÍA-DULANTZI                                                     
01001;0001;*DISEMINADO*                                                          
01001;0002;EGILETA                                                               
01002;0000;AMURRIO                                                               
01002;0001;ALORIA                                                                
01002;0002;AMURRIO                                                               
01002;0003;ARTOMAÑA                                                             
```

## Mezcla de ficheros

Hay un script en Python: [merge.py](./merge.py) (debemos tener instalado [pandas](https://pandas.pydata.org/)) que nos creará el fichero resultado
