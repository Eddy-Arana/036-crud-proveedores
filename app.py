from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'clave-secreta'


# Usuarios para practicar el login.
# Todavía no se utiliza una base de datos.
USUARIOS = {
    "admin": "1234",
    "usuario": "abcd"
}


# Página de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Mostrar proveedores desde PostgreSQL
@app.route('/proveedores/lista')
def lista_proveedores():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("""
        SELECT id, nombre, nit, telefono, correo, direccion, activo, fecha_registro
        FROM proveedores
        ORDER BY id DESC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'index.html',
        proveedores=proveedores
    )

# Crear un nuevo proveedor
@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():

    if request.method == 'POST':

        nombre = request.form['nombre']
        nit = request.form['nit']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']

        activo = request.form.get('activo') == 'on'

        conexion = get_connection()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, nit, telefono, correo, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nombre,
            nit,
            telefono,
            correo,
            direccion,
            activo
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash('Proveedor creado correctamente.', 'success')

        return redirect(url_for('lista_proveedores'))

    return render_template('form.html')

# Editar un proveedor
@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):

    conexion = get_connection()
    cursor = conexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    if request.method == 'POST':

        nombre = request.form['nombre']
        nit = request.form['nit']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']

        activo = request.form.get('activo') == 'on'

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                nit = %s,
                telefono = %s,
                correo = %s,
                direccion = %s,
                activo = %s
            WHERE id = %s
        """, (
            nombre,
            nit,
            telefono,
            correo,
            direccion,
            activo,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash('Proveedor actualizado correctamente.', 'success')

        return redirect(url_for('lista_proveedores'))

    cursor.execute("""
        SELECT id, nombre, nit, telefono, correo, direccion, activo
        FROM proveedores
        WHERE id = %s
    """, (id,))

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    if proveedor is None:
        flash('Proveedor no encontrado.', 'danger')
        return redirect(url_for('lista_proveedores'))

    return render_template(
        'form.html',
        proveedor=proveedor
    )

# Eliminar un proveedor
@app.route('/proveedores/eliminar/<int:id>', methods=['POST'])
def eliminar_proveedor(id):

    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash('Proveedor eliminado correctamente.', 'success')

    return redirect(url_for('lista_proveedores'))

# Registro de clientes
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nit = request.form['nit']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        return render_template(
            'clientes_confirmacion.html',
            nombre=nombre,
            nit=nit,
            correo=correo,
            telefono=telefono,
            direccion=direccion
        )

    return render_template('clientes.html')


# Registro de proveedores
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if request.method == 'POST':
        empresa = request.form['empresa']
        contacto = request.form['contacto']
        nit = request.form['nit']
        tipo = request.form['tipo']
        condicion = request.form['condicion']

        # Si el checkbox está marcado, llega "si".
        # Si no está marcado, no llega ese dato.
        activo = request.form.get('activo', 'No')

        return render_template(
            'proveedores_confirmacion.html',
            empresa=empresa,
            contacto=contacto,
            nit=nit,
            tipo=tipo,
            condicion=condicion,
            activo=activo
        )

    return render_template('proveedores.html')


# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        recordarme = request.form.get('recordarme', 'No')

        if usuario in USUARIOS and USUARIOS[usuario] == password:
            mensaje = f'Bienvenido, {usuario}. Inicio de sesión correcto.'
            tipo = 'success'
        else:
            mensaje = 'Usuario o contraseña incorrectos.'
            tipo = 'danger'

        return render_template(
            'login_resultado.html',
            mensaje=mensaje,
            tipo=tipo,
            usuario=usuario,
            recordarme=recordarme
        )

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)