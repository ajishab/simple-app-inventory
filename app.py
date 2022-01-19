from flask import Flask, request, jsonify
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
  region = db.Column(db.String(4), nullable=False)
  risk = db.Column(db.String(4), nullable=False)
  pii = db.Column(db.boolean)
  pci = db.Column(db.boolean)
  sox = db.Column(db.boolean)
  

  def __init__(self, appname, region, risk, pii, pci, sox):
    self.appname = appname
    self.region = region
    self.risk = risk
    self.pii = pii
    self.pci = pci
    self.sox = sox

db.create_all()

@app.route('/apps/<id>', methods=['GET'])
def get_item(id):
  app = App.query.get(id)
  del app.__dict__['_sa_instance_state']
  return jsonify(app.__dict__)

@app.route('/apps', methods=['GET'])
def get_items():
  items = []
  for item in db.session.query(Item).all():
    del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
  return jsonify(items)

@app.route('/apps', methods=['POST'])
def create_item():
  body = request.get_json()
  db.session.add(Item(body['title'], body['content']))
  db.session.commit()
  return "item created"