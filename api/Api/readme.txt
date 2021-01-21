-hacer cd en folder de api :
	-python -m pip install virtualenv
	-python -m venv venv // esto te crea el virtualenv de python
	-python3 -m virtualenv -p python venv
	- venv/Scripts/activate // esto es para activar el virtualenv
	-Python -m pip install -r requirements.txt
-Configurar el .env
	-vim .env //tendra que salir  FLASK_APP=api.py FLASK_ENV=development
		*Para escribir tienes que dar un "esq" y luego para dejar de escribir igual
		* luego pones :wq // con esto haces write y sales
-Luego para corre el back es 
	- Flask run 
	
