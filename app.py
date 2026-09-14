from flask import Flask, render_template, request

app = Flask(__name__)


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