# FLASK_APP=app.py FLASK_DEBUG=1 python3 -m flask run


from models import User, Discussion, Message, app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import desc, asc
from utils import validate_password
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'




@app.route('/')
def index():
	discussions = Discussion.query.all()
	return render_template('index.html', discussions=discussions)


@app.route('/home/<int:discussion_id>',methods=['GET', 'POST'])
def home(discussion_id):
	
	if request.method=='POST':
		user=User.query.filter_by(username=session['username']).first()
		mon_message=Message(text=request.form['text'], discussion_id=discussion_id, user_id=user.id)
		db.session.add(mon_message)
		db.session.commit()
	
	messages = Message.query.filter_by(discussion_id=discussion_id).order_by(desc(Message.date)).all()
	discussion = Discussion.query.filter_by(id=discussion_id).first()	
		
	for message in messages:
		message.user=User.query.filter_by(id=message.user_id).first()
		print(message.user)

	
	return render_template('home.html', messages=messages, discussion=discussion )



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user = User(
			username = request.form['username'], 
			password = request.form['password']
			)
		db.session.add(user)
		db.session.commit()
		session['username']=request.form['username']
		return redirect(url_for('index'))

	return render_template('signup.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
	print(session)
	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		user=User.query.filter_by(username=request.form['username'], password=request.form['password']
		).first()
		if user:
			session['username'] = request.form['username']
			return redirect(url_for('index'))

		flash('Invalid credentials')
	return render_template('login.html', session=session)	


# Pour demain creer un systeme de logout
# On ne veut pas afficher de template
# On veut s'assurer que les infos de l'utilisateur ne sont plus dans la session
# Renvoyer l'index
# Mettre un lien log out dans la barre de navigation
# Ce lien apparait uniquement si l'uitlisateur est logged in
@app.route('/logout/')
def logout():
	print(session)
	if 'username' in session:
		session.pop('username', None)
	print(session)
	return redirect(url_for('index'))
# git status hello world

# @app.route('/profile/<int:user_id>/password', methods=['POST'])
# def password_update(user_id):
# 	 user = User.query.filter_by(
# 	  username=session['username'],
# 	  password=request.form['old-password']
# 	 ).first()
# 	​
# 	 if user:
# 	  user.password = request.form['new-password']
# 	  db.session.commit()
# 	 else:
# 	  flash('Invalid password')
# 	​
# 	 return redirect( url_for('profile', user_id=user_id) )

@app.route('/profile/<int:user_id>/username', methods=['POST'])
def username_update(user_id):
  new_username = request.form['new-username']
  if User.query.filter_by(username=new_username).first():
    flash('Username is already taken')
  else:
    user = User.query.filter_by(id=user_id).first()
    user.username = new_username
    db.session.commit()
    session['username'] = new_username

  return redirect( url_for('profile', user_id=user_id) )
