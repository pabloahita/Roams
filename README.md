El proyecto de esta prueba técnica está compuesto de la siguiente manera:
<ul>
  <li><b>Carpeta app: </b>En esta carpeta se encuentran los ficheros .py que se han utilizado para crear la API, los cuales son:
  <ul>
    <li><b><i>main.py:</i></b> Es el archivo principal que se encarga de montar la API de Swagger y de instalar todos los módulos necesarios en caso de que no se utilicen los ejecutables de la carpeta dist</li>
    <li><b><i>dbhelper.py:</i></b> Es el archivo que contiene los métodos estáticos para realizar operaciones hacia la base de datos</li>
    <li><b><i>cliente.py:</i></b> Es el archivo que contiene la clase que conforma el modelo cliente basado en BaseModel con los validadores de PyDantic, según se estableció en esta prueba técnica: <i>Nombre, DNI, email y capital_solicitado</i></li>
  </ul>
  </li>
  <li><b>Carpeta dist: </b> Es la carpeta que contiene los ejecutables, <b><i>.exe</i></b> en el caso de Windows y <b><i>sin extensión</i></b> en el caso de Linux o Mac</li>
</ul>

Para poder realizar la ejecución de este proyecto, no es necesario realizar instalación alguna, ya que los ejecutables se han creado con pyinstaller mediante el fragmento de código
````
pyinstaller --onefile --hidden-import=subprocess --hidden-import=sys --hidden-import=flask --hidden-import=pydantic --hidden-import=flask_restx --hidden-import=re --hidden-import=sqlite3 --hidden-import=cliente --hidden-import=dbhelper --hidden-import=email_validator --hidden-import=importlib_resources.trees --add-data "basededatos.db;." ./app/main.py
````
en el caso de Windows y 
````
pyinstaller --onefile --hidden-import=subprocess --hidden-import=sys --hidden-import=flask --hidden-import=pydantic --hidden-import=flask_restx --hidden-import=re --hidden-import=sqlite3 --hidden-import=cliente --hidden-import=dbhelper --hidden-import=email_validator --hidden-import=importlib_resources.trees --add-data="basededatos.db:." ./app/main.py
````
en el caso de Linux o Mac, todo ello desde la carpeta raíz de este proyecto.
Por lo tanto, se puede ejecutar el proyecto de las siguientes maneras:
<ul>
  <li><b>En Windows</b> debemos dirigirnos desde el explorador a la carpeta <b><i>dist</i></b> y luego presionar sobre <b><i>main.exe</i></b>. Aparecerá la ventana de terminal o Símbolo de Sistema del equipo, por lo que sólo quedaría esperar un poco a que salga el enlace de la IP de localhost para poder probar los endpoints.</li>
  <li><b>En Linux</b> debemos abrir el terminal en el directorio raíz e introducir el comando 
    ````
    ./dist/main/
    ````
    , por lo que, de igual manera, sólo quedaría esperar un poco a que salga el enlace de la IP de localhost para poder probar los endpoints.</li>
</ul>
