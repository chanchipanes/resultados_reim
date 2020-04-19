import pymysql
from datetime import datetime

def get_from_db():
    db = pymysql.connect("ulearnet.org","reim_ulearnet","KsclS$AcSx.20Cv83xT","ulearnet_reim_pilotaje")
    cursor = db.cursor()
    return cursor

#INICIO QUERYS GENERALES

def get_date_param(request):

    date = ''

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_inicio >= TIMESTAMP("' + start + '") && a.datetime_termino <= TIMESTAMP("' + end + '")) &&'

    return date

def get_date_param_alumno_respuesta_actividad(request):

    date = ''

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("' + start + '") && a.datetime_touch <= TIMESTAMP("' + end + '")) &&'

    return date
    
def get_date_param_tiempoxactividad(request):

    date = ''

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.inicio >= TIMESTAMP("' + start + '") && a.final <= TIMESTAMP("' + end + '")) &&'

    return date

def get_time_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND c.id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND co.id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = "SELECT u.id, concat(nombres ,' ', apellido_paterno , ' ',apellido_materno) as nombre_alumno, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, datetime_inicio,datetime_termino))/60)) as total_horas, co.nombre as Colegio, concat(n.nombre, c.nombre) as Curso FROM asigna_reim_alumno a, usuario u, pertenece p , nivel n , curso c, colegio co WHERE" + date
    final_base = ' n.id=p.nivel_id and p.curso_id = c.id and  a.usuario_id = u.id and p.usuario_id=u.id and co.id = p.colegio_id AND p.colegio_id IN (SELECT colegio_id FROM pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND p.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base

def get_session_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'

    return start_base + final_base
#sesiones tam
def get_session_PS_query(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param(request)

    start_base = 'SELECT a.sesion_id AS Sesiones FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' '

    return start_base + final_base

def get_touch_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += ' AND a.id_actividad=' + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.id_user = " + request.GET.get('student')
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY id_user'

    return start_base + final_base

def get_alumnos(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.usuario_id) AS Sesiones, b.colegio_id, b.curso_id FROM asigna_reim_alumno a, usuario u, pertenece b WHERE' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
    cursor.execute(start_base + final_base)
    usuarios = str(((len(cursor.fetchall())*40)+20))
    return usuarios 

# FIN QUERYS GENERALES



#INICIO QUERYS DÍA MUNDIAL


###JUEGO LABERINTO###

#COLISIONES---USE get_colision_co

#VECES QUE CAYÓ
def get_fall_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 4065 or id_elemento=4075 or id_elemento=4085) and correcta=2 group by id_elemento '
    return start_base + final_base

#VECES QUE COLISIONO CON EL MURO
def get_colision_wall():
    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 4064 or id_elemento=4074 or id_elemento=4084) group by id_elemento '
    return start_base + final_base

#VECES QUE TERMINO UN LAB
def get_complete_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 4087 or id_elemento=4088 or id_elemento=4089 or id_elemento=4090 or id_elemento=4091 or id_elemento=4092) group by id_elemento '
    return start_base + final_base

#VECES QUE SALIO DE LA ACTIVIDAD LAB
def get_out_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 4063 or id_elemento=4073 or id_elemento=4083) group by id_elemento '
    return start_base + final_base

#VECES QUE GANO EN LAB FACIL
def get_fruiteasy_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and id_elemento = 4087 group by id_elemento '
    return start_base + final_base

#VECES QUE GANO EN LAB MEDIO
def get_fruitmed_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and id_elemento = 4088 group by id_elemento '
    return start_base + final_base

#VECES QUE GANO EN LAB DIFICIL
def get_fruithard_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and id_elemento = 4089 group by id_elemento '
    return start_base + final_base

#VECES QUE PIERDE EN LAB FACIL
def get_fastfoodeasy_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4090 or id_elemento=4062 or id_elemento=4063) group by id_elemento '
    return start_base + final_base

#VECES QUE PIERDE EN LAB MEDIO
def get_fastfoodmed_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4091 or id_elemento=4072 or id_elemento=4073) group by id_elemento '
    return start_base + final_base

#VECES QUE PIERDE EN LAB DIFICL
def get_fastfoodhard_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4092 or id_elemento=4082 or id_elemento=4083) group by id_elemento '
    return start_base + final_base

### FIN JUEGO LABERINTO ###


### JUEGO RÍO Y OCEANO ###

#VECES QUE RECOGIO BASURA EN OCEANO
def get_TrashOcean_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4100 or id_elemento=4101 or id_elemento=4102 or id_elemento=4103 or id_elemento=4104) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO BASURA EN RIO
def get_TrashRiver_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4114 or id_elemento=4115 or id_elemento=4116 or id_elemento=4117 or id_elemento=4118) group by id_elemento '
    return start_base + final_base

#VECES QUE SALVO ANIMALES EN OCEANO
def get_OceanAnimals_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4105 or id_elemento=4106 or id_elemento=4107 or id_elemento=4108) group by id_elemento '
    return start_base + final_base

#VECES QUE SALVO ANIMALES EN RIO
def 01(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4110 or id_elemento=4111 or id_elemento=4112 or id_elemento=4113) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO BOLSAS DE BASURA
def get_Bag_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4100 or id_elemento=4114) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO BOTELLAS
def get_Bottle_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4101 or id_elemento=4115) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO MANCHA
def get_Stain_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4102 or id_elemento=4116) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO RED
def get_Red_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4103 or id_elemento=4117) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO ZAPATOS
def get_Shoes_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4104 or id_elemento=4118) group by id_elemento '
    return start_base + final_base

#VECES QUE RECOGIO BASURA EN EL TIEMPO
def get_element_TrashinTime_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 4100 OR a.id_elemento= 4101 OR a.id_elemento= 4102 OR a.id_elemento= 4103 OR a.id_elemento= 4104 OR a.id_elemento= 4114 OR a.id_elemento= 4115 OR a.id_elemento= 4116 OR a.id_elemento= 4117 OR a.id_elemento= 4118)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

#VECES QUE SALVO ANIMALES EN EL TIEMPO
def get_element_AnimalsinTime_query(request):
    
    query_params = ''
    date = ''
    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 4105 OR a.id_elemento= 4106 OR a.id_elemento= 4107 OR a.id_elemento= 4108 OR a.id_elemento= 4110 OR a.id_elemento= 4111 OR a.id_elemento= 4112 OR a.id_elemento= 4113)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base
### FIN JUEGO RIO Y OCEANO ###

### INICIO JUEGO LUCES ###

#TRAER CORRECTAS LUCES

def get_AllLights_light(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4094 or id_elemento=4096 or id_elemento=4098) group by id_elemento '
    return start_base + final_base

#TRAER TODOS LOS TOUCHS
def get_AllTouchs_light(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params
    return start_base + final_base

#CUANTAS VECES ABANDONO ACTIVIDAD
def get_incompleta_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')

    date = get_date_param_tiempoxactividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.causa=2,1,NULL)) completas, count(if(a.causa=1,1,NULL)) incompletas, count(if(a.causa=0,1,NULL)) inactividad  FROM tiempoxactividad a, usuario u, pertenece b WHERE ' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id' + query_params + ' GROUP BY u.apellido_paterno'
    return start_base + final_base

#CUANTAS VECES JUGO LA ACTIVIDAD (relacionada a la query de arriba)

### FIN JUEGO LUCES ###

### INICIO JUEGO ABEJAS ###

#CUANTAS VECES NIÑO TOCA LA MIEL
def get_HONEYCOMB_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4153) group by id_elemento '
    return start_base + final_base

#CUANTAS VECES NIÑO JUEGA ACTIVIDAD (misma query que get incompleta)

#CUANTAS VECES NIÑO SE CAE
def get_Ground_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4154) group by id_elemento '
    return start_base + final_base

#CUANTAS VECES NIÑO CHOCA CON AVISPA Y OSO
def get_Enemies_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4155) group by id_elemento '
    return start_base + final_base

#CUANTAS VECES NIÑO ABANDONA ACTIVIDAD (misma que incompleta)

### FIN JUEGO ABEJAS ###

### INICIO JUEGO ANIMALES ###

#CUANTOS ANIMALES SALVO EL NIÑO (GENERAL)
def get_AnimalsGeneral_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4034 or id_elemento=4035 or id_elemento=4036 or id_elemento=4037 or id_elemento=4038 or id_elemento=4039 or id_elemento=4041 or id_elemento=4042 or id_elemento=4043 or id_elemento=4044 or id_elemento=4045 or id_elemento=4046 or id_elemento=4048 or id_elemento=4049 or id_elemento=4050 or id_elemento=4051 or id_elemento=4052 or id_elemento=4053 or id_elemento=4054 or id_elemento=4055 or id_elemento=4056) group by id_elemento '
    return start_base + final_base

#COMPLETAS E INCOMPLETAS (MISMA QUERY QUE INCOMPLETA)

#CUANTOS ANIMALES SALVO EL NIÑO POR NIVEL EN EL TIEMPO (ANTARTICA)
def get_element_AnimalsinTimeAntartic_query(request):
    
    query_params = ''
    date = ''
    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (id_elemento=4034 or id_elemento=4035 or id_elemento=4036 or id_elemento=4037 or id_elemento=4038 or id_elemento=4039)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

#CUANTOS ANIMALES SALVO EL NIÑO POR NIVEL EN EL TIEMPO (JUNGLE)
def get_element_AnimalsinTimeJungle_query(request):
    
    query_params = ''
    date = ''
    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (id_elemento=4041 or id_elemento=4042 or id_elemento=4043 or id_elemento=4044 or id_elemento=4045 or id_elemento=4046)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

#CUANTOS ANIMALES SALVO EL NIÑO POR NIVEL EN EL TIEMPO (DESERT)
def get_element_AnimalsinTimeDesert_query(request):
    
    query_params = ''
    date = ''
    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (id_elemento=4048 or id_elemento=4049 or id_elemento=4050 or id_elemento=4051 or id_elemento=4052 or id_elemento=4053 or id_elemento=4054 or id_elemento=4055 or id_elemento=4056)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base


### FIN JUEGO ANIMALES ###

### INICIO JUEGO ARBOL ###

#CUANTAS INSTRUCCIONES SIGUIÓ EL NIÑO
def get_Generalnstruccions_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4121 or id_elemento=4122 or id_elemento=4122 or id_elemento=4123 or id_elemento=4124 or id_elemento=4125 or id_elemento=4126 or id_elemento=4127 or id_elemento=4128 or id_elemento=4129 or id_elemento=4130 or id_elemento=4131 or id_elemento=4132) group by id_elemento '
    return start_base + final_base

#CUANTAS INSTRUCCIONES NO SIGUIÓ EL NIÑO (dato creado entre total de veces que creció el arbol x la cantidad de instrucciones correctas para el crecimiento menos el total de instrucciones seguidas)

#CUANTAS VECES JUGÓ EL NIÑO (MISMA QUERY QUE INCOMPLETAS)

#CUANTAS VECES CRECIÓ EL ARBOL
def get_TreeGrow_lab(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Agujero from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento=4156) group by id_elemento '
    return start_base + final_base

### FIN JUEGO ARBOL ### 

#FIN QUERYS DÍA MUNDIAL


#INICIO QUERYS CLEAN OCEAN

#CANTIDAD DE COLISIONES
def get_colision_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS colisiones, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.correcta=3 GROUP BY u.id'
    return start_base + final_base


#CORRECTAS E INCORRECTAS

def get_corrects_incorrects_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.id_user = " + request.GET.get('student')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=1,1,NULL)) Correctas, count(if(correcta=0,1,NULL)) Incorrectas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    return start_base + final_base

#CORRECTAS GENERALES
def get_corrects_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=1,1,NULL)) Correctas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    return start_base + final_base

def get_incorrects_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(correcta=0,1,NULL)) Incorrectas FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=0 GROUP BY u.id'
    return start_base + final_base

def get_jumps_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=4 GROUP BY u.id'
    return start_base + final_base

def get_analytics_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if((a.id_actividad=3007 and correcta=1) or (a.id_actividad=3004 and correcta=1) or (a.id_actividad=3002 and correcta=1),1,NULL)) CorrectaAct1, count(if((a.id_actividad=3003 and correcta=1) or (a.id_actividad=3005 and correcta=1) ,1,NULL)) CorrectaAct2 FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.id'
    return start_base + final_base

def get_incorrects_act1_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=0 AND a.id_actividad = 3004 GROUP BY u.id'
    return start_base + final_base

def get_corrects_act2_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=1 AND a.id_actividad = 3007 GROUP BY u.id'
    return start_base + final_base

def get_incorrects_act2_co(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS saltos, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND a.correcta=0 AND a.id_actividad = 3007 GROUP BY u.id'
    return start_base + final_base

def get_exit_lab(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre as Destino, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' e.id=a.id_elemento and id_user="' + request.GET.get('student') + '" AND id_actividad=3004 and a.id_elemento>=3049 and a.id_elemento<=3052 group by a.id_elemento'
    return start_base + final_base

def get_touch_animals_co(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Animal from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + ' and (id_elemento = 3012 or (id_elemento >= 3021 && id_elemento <= 3039) or (id_elemento >=3061 && id_elemento <= 3064) or id_elemento=3017 or id_elemento=3056) and correcta=2 group by id_elemento'
    print (start_base + final_base)
    return start_base + final_base

def get_touch_trash_co(request):

    query_params = ''

    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT id_user, e.nombre, count(id_elemento) as Animal from alumno_respuesta_actividad a, elemento e WHERE' + date
    final_base = ' a.id_elemento=e.id and id_user="' + request.GET.get('student') + '" ' + query_params + '  and (id_elemento = 3019 or (id_elemento >= 3040 and id_elemento <= 3044)) and correcta=2 group by id_elemento '
    return start_base + final_base

def get_cant_touch_act_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT o.id, o.nombre, count(o.id) AS actividades FROM actividad o, alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_actividad=o.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND o.id>3000 AND o.id<3007 GROUP BY o.id'
    return start_base + final_base

def get_colision_trash(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = ' a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=3 group by id_elemento;'
    return start_base + final_base

def get_touch_all_animals(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and (id_elemento = 3012 or (id_elemento >= 3021 && id_elemento <= 3039) or (id_elemento >=3061 && id_elemento <= 3064) or id_elemento=3017 or id_elemento=3056) and correcta=2 group by id_elemento;'
    return start_base + final_base

def get_touch_all_trash(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=2 and (id_elemento=3019 or (id_elemento>=3041 and id_elemento<=3044) or (id_elemento>=3068 and id_elemento<=3069)) group by id_elemento;'
    return start_base + final_base

def get_exits_lab_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and id_actividad=3004 and (id_elemento>=3049 and id_elemento<=3052) group by id_elemento;'
    return start_base + final_base

def get_buttons_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_elemento, e.nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and correcta=2 and (id_elemento=3013 or id_elemento=3067 or (id_elemento>=3000 and id_elemento<=3002) or (id_elemento>=3007 and id_elemento<=3009)) group by id_elemento;'
    return start_base + final_base

def get_trash_clean_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select id_user, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(e.id) as Cantidad FROM alumno_respuesta_actividad a, elemento e, usuario u, pertenece b where' + date
    final_base = '  a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' and id_elemento=3041 group by id_user;'
    return start_base + final_base

def get_corrects_student_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    # if request.GET.get('course') and request.GET.get('course') != '0':
    #     query_params += " AND b.curso_id = " + request.GET.get('course')
    # if request.GET.get('school') and request.GET.get('school') != '0':
    #     query_params += " AND b.colegio_id = " + request.GET.get('school')
    # if request.GET.get('activity') and request.GET.get('activity') != '0':
    #     query_params += " AND a.id_actividad = " + request.GET.get('activity')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'select a.id_user, ac.nombre as Actividad, count(if(a.correcta=1,1,NULL)) Correcta, count(if(a.correcta=0,1,NULL)) Incorrecta FROM alumno_respuesta_actividad a, actividad ac where' + date
    final_base = '  ac.id=a.id_actividad && a.id_user="' + request.GET.get('student') + '" ' + query_params + ' and a.id_actividad>= 3002 and a.id_actividad<=3007 group by ac.nombre;'
    return start_base + final_base


def get_time_act_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND a.usuario_id = " + request.GET.get('student')

    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))/60)) as total_min FROM tiempoxactividad a, usuario u, pertenece b , nivel n , curso c, colegio co WHERE' + date
    final_base = ' n.id=b.nivel_id and b.curso_id = c.id and a.usuario_id = u.id and b.usuario_id=u.id and co.id = b.colegio_id' + query_params + ' group by u.id;'
    return start_base + final_base


#FIN QUERYS CLEAN OCEAN

#INICIO QUERYS MUNDO ANIMAL 
def get_piezas(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS piezas, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' and ((a.correcta>9 and a.correcta<100) || (a.id_elemento = 35 and a.id_actividad = 5) || (a.id_elemento = 32 and a.id_actividad = 6)) GROUP BY u.id;'
    return start_base + final_base

def get_malas(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.correcta) AS malas, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND (a.correcta=0 OR a.correcta>999) GROUP BY u.id'
    return start_base + final_base

def get_animals(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += " AND u.id = " + request.GET.get('student')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT e.id, e.nombre, count(e.id) AS animales FROM elemento e, alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_elemento=e.id && a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND e.id>10 AND e.id<26 GROUP BY e.id'
    return start_base + final_base

def get_actividades(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param(request)

    start_base = 'SELECT o.id, o.nombre, count(o.id) AS cantidad FROM actividad o WHERE'
    final_base = ' o.id>0 AND o.id<8 '
    cursor.execute(start_base + final_base)
    actividades = str(((len(cursor.fetchall())*40)+20))
    return actividades 
    
def get_cant_touch(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT o.id, o.nombre, count(o.id) AS actividades FROM actividad o, alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_actividad=o.id && a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND o.id>0 AND o.id<8 GROUP BY o.id'
    return start_base + final_base

def get_interaccion(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT c.usuario_id, concat(d.nombres, " ", d.apellido_paterno," ", d.apellido_materno) as Nombre , count(a.id_reim) as Cantidad FROM alumno_respuesta_actividad a, `Avatar-Sesion` b, asigna_reim_alumno c, usuario d, pertenece e where' + date
    final_base = ' e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND c.usuario_id = d.id and c.usuario_id = e.usuario_id and a.correcta = b.elemento_id and b.asigna_reim_alumno_sesion_id = c.sesion_id and a.datetime_touch > c.datetime_inicio and a.datetime_touch < c.datetime_termino and correcta >9 and correcta<100 group by c.usuario_id;'
    return start_base + final_base

def get_tiempoact(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND e.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND e.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')
        
    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT a.actividad_id, b.nombre, round((sum(timestampdiff(minute, inicio, final))/60)) as tiempo FROM tiempoxactividad a, actividad b, pertenece e where'
    final_base = ' e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND a.actividad_id = b.id group by actividad_id;'
    return start_base + final_base

# Avance en query tiempo total del curso por actividad
# SELECT t.id, t.inicio, t.final, t.actividad_id, t.usuario_id, (sum(timestampdiff(minute, inicio, final)))/60 FROM tiempoxactividad t, actividad b, pertenece e where e.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="163465639") AND e.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "163465639")) AND t.reim_id = 1 AND e.curso_id = 5 AND e.colegio_id = 3 AND t.actividad_id = b.id group by usuario_id;

def get_analytics1_co(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
     
    date = get_date_param_alumno_respuesta_actividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=7,1,NULL)) Actividad1, count(if(a.id_elemento=8,1,NULL)) Actividad2, count(if(a.id_elemento=9,1,NULL)) Actividad3, count(if(a.id_elemento=10,1,NULL)) Actvidad4, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b where' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.id'
    return start_base + final_base

def get_tiempo_total_act(request):
    cursor = get_from_db()
    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')

    date = get_date_param_tiempoxactividad(request)

    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, IF (ROUND((SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))))/60<1, 1,ROUND(SUM(TIMESTAMPDIFF(SECOND, a.inicio, a.final))/60)) as total_min FROM tiempoxactividad a, usuario u, pertenece b , nivel n , curso c, colegio co WHERE' + date
    final_base = ' n.id=b.nivel_id and b.curso_id = c.id and a.usuario_id = u.id and b.usuario_id=u.id and co.id = b.colegio_id' + query_params + ' group by u.id;'
    return start_base + final_base

def get_audios(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')


    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(a.id_elemento) AS audios, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user= u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON pertenece.usuario_id = usuario.id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' AND (a.id_elemento = 28 OR a.id_elemento = 36 OR a.id_elemento = 48 OR a.id_elemento = 52 OR a.id_elemento = 63 OR a.id_elemento = 64 OR a.id_elemento = 65 OR a.id_elemento = 66 ) GROUP BY u.id'
    return start_base + final_base



#FIN QUERYS MUNDO ANIMAL 

#INICIO QUERYS PLUS SPACE
def get_completa_incompleta_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.reim_id = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.actividad_id = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.usuario_id=' + request.GET.get('student')

    date = get_date_param_tiempoxactividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.causa=2,1,NULL)) completas, count(if(a.causa=1,1,NULL)) incompletas, count(if(a.causa=0,1,NULL)) inactividad  FROM tiempoxactividad a, usuario u, pertenece b WHERE ' + date
    final_base = ' a.usuario_id= u.id && b.usuario_id = a.usuario_id' + query_params + ' GROUP BY u.apellido_paterno'
    return start_base + final_base
def get_elementos_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=2018,1,NULL)) planeta, count(if(a.id_elemento=2019,1,NULL)) planetaCS, count(if(a.id_elemento=2020,1,NULL)) planetaCA , count(if(a.id_elemento=2021,1,NULL)) estrella, count(if(a.id_elemento=2022,1,NULL)) supernova, count(if(a.id_elemento=2023,1,NULL)) nebulosa, count(if(a.id_elemento=2024,1,NULL)) galaxia FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base

def get_elementos_alu_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = 'SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user' + query_params + ' AND (a.id_elemento=2018 OR a.id_elemento=2019 OR a.id_elemento=2020 OR a.id_elemento=2021 OR a.id_elemento=2022 OR a.id_elemento=2023 OR a.id_elemento=2024) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base
    
def get_construccion_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND ( a.id_elemento=2018 OR a.id_elemento=2019 OR a.id_elemento=2020 OR a.id_elemento=2021 OR a.id_elemento=2022 OR a.id_elemento=2023 OR a.id_elemento=2024) '
    
    return start_base + final_base
def get_saltos_analitica_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento=2070 '
    
    return start_base + final_base
def get_colisiones_analitica_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS ocurrecias FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND (a.id_elemento=2091 OR a.id_elemento=2092 OR a.id_elemento=2093 OR a.id_elemento=2094 OR a.id_elemento=2095 OR a.id_elemento=2096 OR a.id_elemento=2097 OR a.id_elemento=2098) GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'
    
    return start_base + final_base
def get_puzzle_PS(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND a.id_elemento= 2128 '
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT u.id, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

def get_ingreso_puzzle_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 
    

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user ' + query_params + ' AND a.id_elemento=2031' 
    
    return start_base + final_base

def get_move_element_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')
    print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, CEILING(a.fila/100), CEILING(a.columna/100) FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' AND (a.id_elemento= 2133 OR a.id_elemento= 2134 OR a.id_elemento= 2135 OR a.id_elemento= 2136 OR a.id_elemento= 2137 OR a.id_elemento= 2138 OR a.id_elemento= 2139)'

    return start_base + final_base

#LABERINTO
def get_posicionamiento_PS(request):

    query_params = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params += " AND a.id_reim = " + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('activity') and request.GET.get('activity') != '0':
        query_params += " AND a.id_actividad = " + request.GET.get('activity')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student') 

    date = get_date_param_alumno_respuesta_actividad(request)
    start_base = ' SELECT u.id, concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, count(if(a.id_elemento=2099,1,NULL)) tierra, count(if(a.id_elemento=2100,1,NULL)) neptuno, count(if(a.id_elemento=2101,1,NULL)) jupiter , count(if(a.id_elemento=2102,1,NULL)) saturno, count(if(a.id_elemento=2103,1,NULL)) urano, count(if(a.id_elemento=2104,1,NULL)) venus, count(if(a.id_elemento=2105,1,NULL)) mercurio, count(if(a.id_elemento=2106,1,NULL)) marte FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE ' + date
    final_base = '  a.id_user= u.id && b.usuario_id = a.id_user and a.correcta = 1 ' + query_params + ' GROUP BY u.apellido_paterno'
    
    return start_base + final_base

def get_element_colission_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 2091 OR a.id_elemento= 2092 OR a.id_elemento= 2093 OR a.id_elemento= 2094 OR a.id_elemento= 2095 OR a.id_elemento= 2096 OR a.id_elemento= 2097 OR a.id_elemento= 2098)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

def get_element_colission_alu_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school') + ' AND (a.id_elemento= 2091 OR a.id_elemento= 2092 OR a.id_elemento= 2093 OR a.id_elemento= 2094 OR a.id_elemento= 2095 OR a.id_elemento= 2096 OR a.id_elemento= 2097 OR a.id_elemento= 2098)'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base

#ALTERNATIVAS
def get_jump_alternativas_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2070 AND a.correcta = 1'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    
    #print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

def get_jump_alternativas_alu_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2070 AND a.correcta = 1'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base    

#CUIDA
def get_acierto_cuida_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2120'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    
    #print(query_params)

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT u.id, concat(u.nombres ," " , u.apellido_paterno ," " , u.apellido_materno) as nombre, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user && b.colegio_id IN (SELECT colegio_id from pertenece INNER JOIN usuario ON usuario.id = pertenece.usuario_id WHERE username="' + request.user.username + '") AND b.curso_id IN (SELECT curso_id FROM pertenece WHERE usuario_id = (SELECT id FROM usuario WHERE username = "' + request.user.username + '"))' + query_params + ' GROUP BY u.apellido_paterno'

    return start_base + final_base

def get_acierto_cuida_alu_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')+' AND a.id_elemento= 2120'
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')    

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = 'SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, count(a.id_user) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base
#puzzle
def get_touch_analitica_query(request):
    
    query_params = ''
    date = ''

    if request.GET.get('reim') and request.GET.get('reim') != '0':
        query_params = ' AND a.id_reim=' + request.GET.get('reim')
    if request.GET.get('course') and request.GET.get('course') != '0':
        query_params += " AND b.curso_id = " + request.GET.get('course')
    if request.GET.get('school') and request.GET.get('school') != '0':
        query_params += " AND b.colegio_id = " + request.GET.get('school')
    if request.GET.get('student') and request.GET.get('student') != '0':
        query_params += ' AND a.id_user=' + request.GET.get('student')

    if request.GET.get('start') and (request.GET.get('start') != 'dd/mm/aaaa') and request.GET.get('end') and (request.GET.get('end') != 'dd/mm/aaaa'):
        start = str(datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date())
        end = str(datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date())
        start += " 00:00:00.000000"
        end += " 23:59:59.000000"
        date = ' (a.datetime_touch >= TIMESTAMP("'+ start + '") && a.datetime_touch <= TIMESTAMP("' + end  + '")) &&'

    start_base = ' SELECT  concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre, concat(day(datetime_touch),"/",month(datetime_touch),"/", year(datetime_touch)) AS fecha, COALESCE(round(count((if(a.id_elemento=2128,1,null)))/count((if (a.id_elemento=2031,1,null)))),0) AS CantidadTouch, b.colegio_id, b.curso_id FROM alumno_respuesta_actividad a, usuario u, pertenece b WHERE' + date
    final_base = ' a.id_user = u.id && b.usuario_id = a.id_user ' + query_params + ' GROUP BY day(a.datetime_touch) ORDER BY a.datetime_touch ASC'

    return start_base + final_base 

def get_name_student(request):
    start_base = ' SELECT concat(u.nombres ," ", u.apellido_paterno ," ", u.apellido_materno) as nombre FROM  usuario u WHERE u.id= ' + request.GET.get('student')

    return start_base
  
#FIN QUERY PLUS SPACE------------------------