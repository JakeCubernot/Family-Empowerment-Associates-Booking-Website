from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user #When user is logged in, current_user will retrieve all data
from .models import User, Note, Therapist, Admin
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
    therapist1 = Therapist.query.all()
    admin = Admin.query.all()
    return render_template('control_panel.html', user=current_user, user1=user1, therapist1=therapist1, admin=admin)

@views.route('/add-therapist', methods = ['GET', 'POST'])
@login_required
def new_therapist():#Adds the Add Therapist form submissions into the Therapist Database
    if request.method == 'POST':
        userid = request.form["id"]
        name = request.form["user_name"]
        email = request.form["user_email"]
        therapist = Therapist.query.filter_by(email=email).first()
        if therapist:
            flash('Already a Therapist', 'error')
        else:
            thera = Therapist(user_id=userid, first_name=name, email=email)
            db.session.add(thera)
            db.session.commit()
            flash('Therapist Added', category='success')
        return redirect(url_for('views.control_panel'))
    return render_template('control_panel.html', user=current_user)

@views.route('/add-admin', methods = ['GET', 'POST'])
@login_required
def new_admin():#Adds the Add Therapist form submissions into the Therapist Database

    if request.method == 'POST':
        userid = request.form["id"]
        email = request.form["email"]
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            flash('Already an Admin', category='error')
        else:
            adm = Admin(user_id=userid,  email=email)
            db.session.add(adm)
            db.session.commit()
            flash('Admin Added', category='success')
        return redirect(url_for('views.control_panel'))
    return render_template('control_panel.html', user=current_user)

@views.route('/delete_admin', methods = ['GET', 'POST'])
@login_required
def delete_admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        remove_admin = Admin.query.get_or_404(admin_id)
        db.session.delete(remove_admin)
        db.session.commit()
        return redirect(url_for('views.control_panel'))
    return render_template('control_panel.html', user=current_user)

@views.route('/delete_therapist', methods = ['GET', 'POST'])
@login_required
def delete_therapist():
    if request.method == 'POST':
        therapist_id = request.form['therapist_id']
        remove_therapist = Therapist.query.get_or_404(therapist_id)
        db.session.delete(remove_therapist)
        db.session.commit()
        return redirect(url_for('views.control_panel'))
    return render_template('control_panel.html', user=current_user)

@views.route('/delete_user', methods = ['GET', 'POST'])
@login_required
def delete_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        admin = Admin.query.filter_by(user_id=user_id).first()
        therapist = Therapist.query.filter_by(user_id=user_id).first()
        if admin:
            flash('User is an Admin', 'error')
        elif therapist:
            flash('User is a Therapist', 'error')
        else:
            remove_user = Therapist.query.get_or_404(user_id)
            db.session.delete(remove_user)
            db.session.commit()
        return redirect(url_for('views.control_panel'))
    return render_template('control_panel.html', user=current_user)
