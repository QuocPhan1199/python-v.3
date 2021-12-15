from flask import render_template
from flask.helpers import flash
from flask import  url_for
from werkzeug.wrappers import request
from app import app
from app.forms import LoaiTinForm, TinForm,LoginForm
from app import db
from app.models import User
from app.models import LoaiTin, Tin,User
# from forms import LoaiTinForm
from flask import redirect
from flask_login import login_user, logout_user
from flask_login import current_user, login_required
from flask import request
from werkzeug.urls import url_decode_stream, url_parse
import os

@app.route('/login',methods = ['GET', 'POST'])
def login():
    #n eu user da login thi redirect den trang index
    if current_user.is_authenticated:
        return redirect('/loaitin')
    form = LoginForm()
    if form.validate_on_submit():
        # Kiem tra user co trong db ko
        # Thong tin tu db  da co chua: form.usename.data
        email = User.query.filter_by(email = form.email.data).first()
        # user ko ton tai
        if email is not None:
            # kiem tra pass co dung ko
            if email.password == form.password.data:
                login_user(email)
                # Xu ly next
                next_page = request.args.get('next')
                if next_page is not None:
                    flash('Next page {}'.format(next_page))
                    if url_parse(next_page).netloc != '':
                        flash('netloc: ' + url_parse(next_page).netloc)
                        next_page = '/loaitin'
                else:
                    next_page = '/loaitin'
                    return redirect(next_page) 
            else :
                flash("Sai mật khẩu.")
                return redirect('/login')
        if email is None:
            flash('Tên đăng nhập không tồn tại! Vui lòng đăng ký.')
            return redirect('/login')           
        return redirect('/login')
    return render_template('admin/login.html', form = form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
@app.route('/loaitin',methods = ['GET', 'POST'])
@login_required
def loaitin():
    if current_user.is_authenticated:
        loaitin = LoaiTin.query.all()
        return render_template('admin/loaitin/loaitin.html',
                            loaitin=loaitin)
    else :
        return redirect('/login')
@app.route('/themloaitin',methods = ['GET', 'POST'])
def themloaitin():
    form = LoaiTinForm()
    if form.validate_on_submit():
        department = LoaiTin(tenloai=form.tenloai.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            flash('Error: department name already exists.')
    return render_template('admin/loaitin/themloai.html',
                           form=form
                          )
@app.route('/sualoai/<int:id>', methods=['GET', 'POST'])
def sualoai(id):
    loaitin = LoaiTin.query.get_or_404(id)
    form = form = LoaiTinForm(obj=loaitin)
    if form.validate_on_submit():
        loaitin.tenloai = form.tenloai.data
        db.session.add(loaitin)
        db.session.commit()
        flash('You have successfully edited the category.')
        return redirect(url_for('loaitin'))
    form.tenloai.data = loaitin.tenloai
    return render_template('admin/loaitin/sualoai.html', 
                           form=form, loaitin = loaitin)
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def xoaloai(id):
    loaitin = LoaiTin.query.get_or_404(id)
    db.session.delete(loaitin)
    db.session.commit()
    flash('You have successfully deleted the role.')
    return redirect(url_for('loaitin'))
    # return render_template(title="Delete Role")
@app.route('/tin',methods = ['GET', 'POST'])
def tin():
    loaitin = LoaiTin.query.all()
    tin = Tin.query.all()
    return render_template('admin/tin/tin.html',tin=tin, loaitin=loaitin)

@app.route('/themtin',methods = ['GET', 'POST'])
def themtin():
    loaitins = LoaiTin.query.all()
    form = TinForm()
    if form.validate_on_submit():
        uploaded_file = request.files['images']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            images = 'static/uploads/' + uploaded_file.filename
            tin = Tin(title=form.tieude.data, content=form.noidung.data, images=images, id_Loaitin=form.loaitin.data, tomtat=form.tomtat.data, status=form.status.data)
            try:
                db.session.add(tin)
                db.session.commit()
                flash('You have successfully added a new department.')
                return redirect(url_for('tin'))
            except:
                flash('Error: department name already exists.')
                db.session.rollback()
                raise 
            finally:
                db.session.close()                  
    return render_template('admin/tin/themtin.html',form=form, loaitins=loaitins)


@app.route('/suatin/<int:id>',methods = ['GET', 'POST'])
def suatin(id):
    loaitins = LoaiTin.query.all()
    tin = Tin.query.get_or_404(id)
    form = TinForm(obj=tin)
    if form.validate_on_submit():
        uploaded_file = request.files['images']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            images = 'static/uploads/' + uploaded_file.filename
            tin.title = form.tieude.data
            tin.content = form.noidung.data
            tin.images = images
            tin.id_Loaitin = form.loaitin.data
            tin.tomtat = form.tomtat.data
            tin.status = form.status.data
            db.session.add(tin)
            db.session.commit()
            flash('You have successfully edited the category.')
            return redirect(url_for('tin'))
    return render_template('admin/tin/suatin.html',form=form, loaitins = loaitins, tin = tin)
@app.route('/xoatin/<int:id>',methods = ['GET', 'POST'])
def xoatin(id):
    tin = Tin.query.get_or_404(id)
    db.session.delete(tin)
    db.session.commit()
    flash('You have successfully deleted the role.')
    return redirect(url_for('tin'))


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    loaitins = db.session.query(LoaiTin).all()
    tins = db.session.query(Tin).all()
    if request.args.get("id")!=None:
        key=request.args.get("id")
        tins = db.session.query(Tin).filter(Tin.id_Loaitin==key).all()
    if request.form.get("search")!=None:
        search = request.form.get("search")
        search = "%{}%" .format(search)
        tins = db.session.query(Tin).filter(Tin.title.like(search)|Tin.tomtat.like(search)).all()
    return render_template('pages/index.html', tins=tins, loaitins = loaitins)

@app.route('/detail', methods=['GET', 'POST'])
def detail():
    loaitins = db.session.query(LoaiTin).all()
    if request.args.get("id")!=None:
        key=request.args.get("id")
        tins = db.session.query(Tin).filter(Tin.id==key).first()
    return render_template('pages/detail.html', tins=tins, loaitins = loaitins)

# @app.route('/noidung', methods=['GET', 'POST'])
# def noidung():
#     titles = db.session.query(LoaiTin).all()
#     if request.args.get("matin")!=None:
#         key=request.args.get("matin")
#         content = db.session.query(Tin).filter(Tin.matin==key).first()
#     return render_template('noidung.html', content=content, titles = titles)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect('/index')
# @app.route('/register',methods = ['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             flash("Tên đăng nhập đã tồn tại. Vui lòng nhập tên khác!")
#             return redirect('/register')
#         if form.confirm.data != form.password.data:
#             flash("Mật khẩu không trùng khớp. Vui lòng nhập lại mật khẩu!")
#             return redirect('/register')
#         else:
#             new_user = User(form.username.data,form.email.data, form.password.data)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Đăng ký thành công!')
#             return redirect('/login')
#     return render_template('register.html', form=form)
# @app.route('/upload')
# def upload():
#     return render_template('upload.html')
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         #uploaded_file.save(uploaded_file.filename)
#         uploaded_file.save("static/" + uploaded_file.filename)
#     return redirect('/index')    