from operator import add
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class App(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  appname = db.Column(db.String(80), nullable=False)
  region = db.Column(db.String(6), nullable=False)
  risk = db.Column(db.String(6), nullable=False)
  pii = db.Column(db.Boolean)
  pci = db.Column(db.Boolean)
  sox = db.Column(db.Boolean)
  

  def __init__(self, id, appname, region, risk, pii, pci, sox):
    self.id = id
    self.appname = appname
    self.region = region
    self.risk = risk
    self.pii = pii
    self.pci = pci
    self.sox = sox

db.create_all()

@app.before_first_request
def add_sample_data():
  db.session.add(App(101, "Core Banking", "GLOBAL", "High", True, False, True ))
  db.session.add(App(102, "Marketing DB", "GLOBAL", "Medium", True, False, False ))
  db.session.add(App(103, "EMEA Printer Manager", "EMEA", "Low", False, False, False ))
  db.session.add(App(104, "Europe Payment Network", "EMEA", "High", True, True, False ))
  db.session.add(App(105, "Asia Payment Network", "APAC", "High", True, True, False ))
  db.session.add(App(106, "US Merchant Connect", "AMER", "Medium", False, True, False ))
  db.session.add(App(107, "Accounting Journal", "GLOBAL", "Medium", False, False, True ))
  db.session.commit()

@app.route('/apps/<appid>', methods=['GET'])
def get_item(id):
  apprecord = App.query.get(id)
  del apprecord.__dict__['_sa_instance_state']
  return jsonify(apprecord.__dict__)

@app.route('/apps', methods=['GET'])
def get_items():
  apprecords = []
  for apprecord in db.session.query(App).all():
    del apprecord.__dict__['_sa_instance_state']
    apprecords.append(apprecord.__dict__)
  return jsonify(apprecords)

@app.route('/apps', methods=['POST'])
def create_item():
  body = request.get_json()
  db.session.add(App(body['id'], body['appname'], body['region'], body['risk'], body['pii'], body['pci'], body['sox']))
  db.session.commit()
  return "app record created"

@app.route('/apps/<appid>', methods=['PUT'])
def update_item(appid):
  body = request.get_json()
  db.session.query(App).filter_by(id=appid).update(
    dict(appname=body['appname'], region=body['region'], risk=body['risk'], pii=body['pii'], pci=body['pci'], sox=body['sox']))
  db.session.commit()
  return "item updated"

@app.route('/apps/<appid>', methods=['DELETE'])
def delete_item(appid):
  body = request.get_json()
  db.session.query(App).filter_by(id=appid).delete()
  db.session.commit()
  return "response deleted"

@app.route('/reset', methods=['GET'])
def reset_db():
  body = request.get_json()
  db.session.query(App).delete()
  db.session.commit()
  add_sample_data()
  return "database reset"


@app.route('/ui')
def get_api():
  print('sending docs')
  return render_template('swaggerui.html')