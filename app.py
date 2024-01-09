from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "BESTSECRETKEYINTHISWORLD"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.globals.update(BOTID = 6894150429)
app.jinja_env.globals.update(BOTNAME = "NewReminderBott")
app.jinja_env.globals.update(BOTDOMAIN = "http://10.8.0.121:5100/")

def ToUnix(date_string):
      try:
            date_object = datetime.strptime(date_string, '%d.%m.%Y')
            unix_timestamp = int(date_object.timestamp())
            
            return unix_timestamp
      
      except ValueError:
            return None


@app.before_request
def make_session_permanent():
    session.permanent = True

def template(tmpl_name, **kwargs):
    telegram = False
    user_id = session.get('user_id')
    username = session.get('name')
    photo = session.get('photo')

    if user_id:
        telegram = True

    return render_template(tmpl_name,
                           telegram = telegram,
                           user_id = user_id,
                           name = username,
                           photo = photo,
                           **kwargs)

@app.route("/")
def index():
    return template("telegram.html")

@app.route("/logout")
def logout():
    session.pop("user_id")
    session.pop("name")
    session.pop("photo")

    return redirect(url_for('index'))

@app.route("/login")
def login():
    user_id = request.args.get("id")
    first_name = request.args.get("first_name")
    photo_url = request.args.get("photo_url")

    session['user_id'] = user_id
    session['name'] = first_name
    session['photo'] = photo_url

    return redirect(url_for('reminder_add', telegram_id=user_id))


@app.route('/reminder_add/<telegram_id>', methods=['GET', 'POST'])
def reminder_add(telegram_id):
      if request.method == 'POST':
            reminder = request.form.to_dict()
            reminder['time'] = ToUnix(reminder['time'])
            print(reminder)

      content = {"title": "Создать напоминание", "telegram_id": telegram_id}
      return render_template("/reminder_add.html", context=content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
