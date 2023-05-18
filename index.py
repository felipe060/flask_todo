from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:XYwWDEPmb53sQD3ezUeH@containers-us-west-35.railway.app/railway?6471'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False     #default é True
db = SQLAlchemy(app)

engine = create_engine('mysql+pymysql://root:XYwWDEPmb53sQD3ezUeH@containers-us-west-35.railway.app/railway?6471', echo=True, query_cache_size=0,
                       connect_args=dict(host='containers-us-west-35.railway.app', port=6471))
#mysql -hcontainers-us-west-35.railway.app -uroot -pXYwWDEPmb53sQD3ezUeH --port 6471 --protocol=TCP railway
#mysql+pymysql://root:felipe008@localhost/flask_zero
#mysql://user:password@host/database

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'tb_todo_rail'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_text = Column(String(100), nullable=False)


#Base.metadata.create_all(engine)


@app.route('/')
def index():
    query = session.execute(text('select * from tb_todo_rail order by task_id desc'))
    return render_template('index.html', query=query)


@app.route('/add', methods=['POST', 'GET'])
def add_task():
    task = request.form.get('name_textarea')
    new_task = Task(task_text=task)
    print('')
    print(f'funcao add task \n'
          f'new task --> {task} \n')
    try:
        session.add(new_task)
        session.commit()
        print('')
        print('task adicionada c sucesso \n')
        return redirect('/')
    except:
        print('')
        print('houve um erro ao adicionar a task \n')
        return redirect('/')


@app.route('/delete/<int:number>')
def delete(number):
    session.execute(text(f'delete from tb_todo_rail where task_id = {number}'))
    session.commit()
    print('')
    print('funcao --> delete')
    print(f'task id {number} deletada c sucesso\n')
    return redirect('/')


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
