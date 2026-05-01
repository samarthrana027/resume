from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/submission',methods = ['GET','POST'])
def submission():
    if request.method == 'POST':
        name = request.form['username']
        return f"Hello, {name}, welcome to Flask!"
    return render_template('name.html')

if __name__ == '__main__':
    app.run(debug = True)