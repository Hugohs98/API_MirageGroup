from flask_mysqldb import MySQL
from main import mysql

def insertUser(cpf,email,senha):
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO users (cpf,email,senha) VALUES (%s,%s,%s)''', (cpf,email,senha))
    mysql.connection.commit()
    cursor.close()

def retrieveUsers():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT cpf, email FROM users''')
    users = cursor.fetchall()
    cursor.close()
    return users

def retrieveLab(labnum): 
    cursor = mysql.connection.cursor()
    cursor.execute(f'''SELECT * FROM laboratorio{labnum} ORDER BY pos''')
    computadores = cursor.fetchall()
    cursor.close()
    return computadores

def retrieveCalls():
    cursor = mysql.connection.cursor()
    cursor.execute(f''' SELECT * FROM chamados ''')
    chamados = cursor.fetchall()
    cursor.close()
    return chamados

def createCall(form, labnum):
    cursor = mysql.connection.cursor()
    pc_id = form.input_numero_pc.data
    email = form.email.data
    pc_problem = form.pc_problem.data
    problem_description = form.problem_description.data
    labnum = str(labnum)
    email = email + "@fatec.sp.gov.br"
    updatePcStatus(labnum, pc_id, pc_problem, problem_description)
    cursor.execute(f''' INSERT INTO chamados (laboratorio_num, pc_id, data_chamado, hora_chamado, autor, problema_tipo, problema_desc) VALUES (%s, %s, CURDATE(), CURRENT_TIME(), %s, %s, %s) ''', (labnum, pc_id, email, pc_problem, problem_description))
    mysql.connection.commit()
    cursor.close()

def finishCall(callnumber):
    cursor = mysql.connection.cursor()
    callnumber = str(callnumber)
    cursor.execute(f''' SELECT * FROM chamados WHERE id = {callnumber} ''')
    chamado = cursor.fetchall()
    cursor.execute(f''' DELETE FROM chamados WHERE id = {callnumber} ''')
    mysql.connection.commit()
    cursor.execute(f''' UPDATE laboratorio{chamado[0][1]} SET pc_problema = NULL, pc_descricao = "O computador está funcionando corretamente"''')
    mysql.connection.commit()
    cursor.close()

def updatePcStatus(labnum, pc_id, pc_problem, problem_description):
    cursor = mysql.connection.cursor()
    cursor.execute(f''' UPDATE laboratorio{labnum} SET pc_problema = %s, pc_descricao = %s WHERE pc_id = %s''', (pc_problem, problem_description, pc_id))
    mysql.connection.commit()
    cursor.close()

def retrieveAccessCode():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT acesso FROM acesso_tecnico ''')
    acesso = cursor.fetchall()
    return acesso

def retrieveComponents(labNum):
     cursor = mysql.connection.cursor()
     cursor.execute(f''' SELECT * FROM componentes WHERE laboratorio = {labNum} ''')
     componentes = cursor.fetchall()
     cursor.close()
     return componentes

def updateComponent(componente, labnum, config):
  cursor = mysql.connection.cursor()
  cursor.execute(f''' UPDATE componentes SET {config} = %s WHERE laboratorio = %s ''', (componente, labnum))
  mysql.connection.commit()
  cursor.close()
