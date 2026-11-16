from flask import Flask, render_template, flash, redirect, url_for, session, request
from datos import computadoras, reservas
from persistencia import cargar_datos, guardar_datos
from prestamos import (liberar_reservas_vencidas, devolver_pc, cancelar_reserva, solicitar_prestamo,
                        crear_reservacion, ZONA, retirar_reserva)
from usuarios import es_alumno, es_admin, existe_usuario
from datetime import datetime, timedelta
from equipos import buscar_software, registrar_necesidad

app = Flask(__name__)
app.secret_key = "Devinmer"  # Clave secreta para sesiones y seguridad
cargar_datos()


@app.before_request #Antes de cada peticion
def antes_de_cada_peticion():
    liberar_reservas_vencidas()
    if "num_control" not in session and request.endpoint not in ("login", "static"):
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            num = int(request.form.get("num_control"))
        except ValueError:
            num = None
        if num is not None and existe_usuario(num):
            session["num_control"] = num
            return redirect(url_for("inicio"))
        flash("Número de control no registrado.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.context_processor
def datos_de_sesion():
    num = session.get("num_control")
    return {"num_control": num, "soy_admin": num is not None and es_admin(num)}


@app.route("/")
def inicio():
    hoy = datetime.now(ZONA).date()
    limite = hoy + timedelta(days=3)
    return render_template("index.html", computadoras=computadoras, reservas=reservas,
                           hoy=hoy.isoformat(), limite=limite.isoformat(),
                           hoy_txt=hoy.strftime("%d/%m/%Y"))


@app.route("/devolver/<id_pc>", methods=["POST"])
def devolver(id_pc):
    ok, mensaje = devolver_pc(id_pc, session["num_control"])
    flash(mensaje, "success" if ok else "danger")
    return redirect(url_for("inicio"))


@app.route("/cancelar/<id_pc>", methods=["POST"])
def cancelar(id_pc):
    ok, mensaje = cancelar_reserva(id_pc, request.form["fecha"], session["num_control"])
    flash(mensaje, "success" if ok else "danger")
    return redirect(url_for("inicio"))

@app.route("/prestamo", methods=["POST"])
def prestamo():
    ok, mensaje = solicitar_prestamo(session["num_control"], request.form["programa"])
    flash(mensaje, "success" if ok else "danger")
    return redirect(url_for("inicio"))

@app.route("/reservar", methods=["POST"])
def reservar():
    ok, mensaje = crear_reservacion(session["num_control"],
                                    request.form["programa"], request.form["fecha"])
    flash(mensaje, "success" if ok else "danger")
    return redirect(url_for("inicio"))

@app.route("/retirar/<id_pc>", methods=["POST"])
def retirar(id_pc):
    ok, mensaje = retirar_reserva(id_pc, session["num_control"])
    flash(mensaje, "success" if ok else "danger")
    return redirect(url_for("inicio"))

@app.route("/buscar")
def buscar():
    programa = request.args.get("programa", "").strip()
    resultados = buscar_software(programa)
    return render_template("buscar.html", programa=programa, resultados=resultados)


@app.route("/necesidad", methods=["POST"])
def necesidad():
    ok, mensaje = registrar_necesidad(session["num_control"], request.form["programa"])
    flash(mensaje, "success" if ok else "danger")
    return redirect(url_for("inicio"))








if __name__ == "__main__": #Al ejecutar el python app.py, name pasa a ser igual a main, y se ejecuta el app.run(debug=True) que inicia el servidor de Flask
    app.run(debug=True)