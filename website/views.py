from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user #When user is logged in, current_user will retrieve all data
from .models import User, Note
from .import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required #Cannot access homepage unless logged in.
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            #current_user can access any field of currently signed in user
            new_note = Note(data=note, user_id=current_user.id) 
            db.session.add(new_note)
            db.session.commit()
            flash('Note is added', category='success')

    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId) #Check if note has that id in the database.
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/book', methods=['GET', 'POST'])
@login_required #Cannot access homepage unless logged in.
def book():
    return render_template('book.html', user=current_user)
    
@views.route('/control_panel', methods=['GET', 'POST'])
@login_required
def control_panel():
    user1 = User.query.all()
    return render_template('control_panel.html', user=current_user,user1=user1)