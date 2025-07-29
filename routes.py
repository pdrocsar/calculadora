from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    tipo = request.form['tipo']
    salario = float(request.form['salario'])
    extras = float(request.form.get('extras', 0))
    bonificaciones = float(request.form.get('bonificaciones', 0))
    descuentos = float(request.form.get('descuentos', 0))
    ausencias = float(request.form.get('ausencias', 0))

    if tipo == 'salario':
        salario_diario = salario / 30
        salario_descuento = salario_diario * ausencias
        ips = salario * 0.09
        sueldo_final = salario + extras + bonificaciones - descuentos - salario_descuento - ips
        return render_template('resultado.html', resultado=round(sueldo_final, 2), detalle="Salario neto estimado")

    else:
        fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], "%Y-%m-%d")
        fecha_egreso = datetime.strptime(request.form['fecha_egreso'], "%Y-%m-%d")
        dias_trabajados = (fecha_egreso - fecha_ingreso).days
        anios = dias_trabajados / 365.25
        meses = dias_trabajados / 30.44

        aguinaldo = (salario / 12) * meses
        vacaciones = (salario / 30) * 15  # vacaciones estándar
        indemnizacion = salario * anios if request.form['causa'] == 'despido' else 0
        preaviso = salario if request.form['causa'] == 'despido' else 0

        total = aguinaldo + vacaciones + indemnizacion + preaviso
        return render_template('resultado.html', resultado=round(total, 2), detalle="Liquidación estimada")
