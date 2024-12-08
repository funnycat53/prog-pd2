import sqlite3
from flask import Flask, render_template, request, redirect
from dati import pievienot_lietotaju, iegut_lietotajus, pievienot_zinu, iegut_zinu, noņemt_dublētos, iegut_statistiku  

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def index():

    noņemt_dublētos()
    lietotaji_no_db = iegut_lietotajus()
    error_message = None

    if request.method == "POST":
        vards = request.form["name"].strip().capitalize()
        uzvards = request.form["lastname"].strip().capitalize()
        lietotajvards = request.form["username"].strip()

        if not vards or not uzvards or not lietotajvards:
            error_message = "Lūdzu, aizpildiet visus laukus!"
            return render_template("index.html", registreti_lietotaji=lietotaji_no_db, error_message=error_message)

        if pievienot_lietotaju(vards, uzvards, lietotajvards):
            dati = f"Pievienots reģistrēts lietotājs - {vards} {uzvards} {lietotajvards}"
        else:
            dati = None
            error_message = f"Kļūda: Lietotājvārds {lietotajvards} jau eksistē!"        
            
        lietotaji_no_db = iegut_lietotajus()
        return render_template("index.html", aizsutitais = dati, registreti_lietotaji = lietotaji_no_db, error_message=error_message)
    return render_template("index.html", registreti_lietotaji = lietotaji_no_db, error_message=error_message)

@app.route("/zinojumi")
def pievienot():
    lietotaji = iegut_lietotajus()
    zina = iegut_zinu()

    return render_template("zinojumi.html", lietotaji = lietotaji, zina = zina)

@app.route("/pievienot/zinojumu", methods=["POST"])
def zinojumi():
    lietotajvards = request.form["lietotajs"] 
    zina = request.form["zinojums"]
    
    # atrod lietotāja ID no lietotājvārda
    lietotaji = iegut_lietotajus()
    for lietotajs in lietotaji:
        if lietotajs[2] == lietotajvards:  # pārbauda vai lietotājvārds ir saskan
            lietotaja_id = lietotajs[3]  # iegūst lietotāja ID
            pievienot_zinu(lietotaja_id, zina)
            break
    
    return redirect("/zinojumi")

@app.route("/statistika")
def statistika():
    statistikas_dati = iegut_statistiku()
    return render_template("statistika.html", statistika=statistikas_dati)

if __name__ == '__main__':
    app.run(debug=True, port = 5000)