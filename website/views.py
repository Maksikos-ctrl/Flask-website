from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Note 
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) 
@login_required
def homepage():
     if request.method == 'POST':
          note = request.form.get('note')

          if len(note) < 1:
              flash('примечание слишком маленькое!', category='error')
          else:
              new_note = Note(data=note, user_id=current_user.id)
              db.session.add(new_note)
              db.session.commit()
              flash('Примечание добавлено!', category='success')    

     return render_template("homepage.html", user=current_user)

@views.route('/remove-note', methods=['POST'])
def remove_note():
    note = json.loads(request.data)
    noteId =  note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.remove(note)
            db.session.commit()

    return jsonify({})

     
