from flask import Flask, render_template, request
import random   
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "cheiameasecreta"
no_of_memes = 290

def top(file_name, nr_elemente):
    f = open(file_name, 'r+')
    a = f.readlines()
    ac = a
    v = []
    for i in range(nr_elemente):
        v.append(str(ac.index(max(ac))))
        del ac[ac.index(max(ac))]
    return v

def replace_line(file_name, line_num, scor_nou):
    f = open(file_name, 'r+')
    a = f.readlines()#(list(map(int, input().split())))    
    a[line_num] = scor_nou
    o = open(file_name, 'w')
    for i in a:
        o.write(i)
    o.close()
def citire_scor(file_name, nr_poza1, nr_poza2):
    f = open(file_name, 'r+')
    a = f.readlines()#(list(map(int, input().split())))    
    poza1_scor = a[nr_poza1].rstrip('\n\r')
    poza2_scor = a[nr_poza2].rstrip('\n\r')
    return poza1_scor, poza2_scor
def poza_expected(poza1_scor, poza2_scor):
    poza1_expected = 1 / (1 + 10 ** ((poza2_scor-poza1_scor)/400))
    poza2_expected = 1 - poza1_expected
    return poza1_expected, poza2_expected
def poza_scornou(scor_curent, expected, castig):
    scor_nou = scor_curent + 500*(castig - expected)
    return scor_nou


@app.route("/", methods=["GET","POST"])
def home():
    nr_poza1 = random.randint(0,no_of_memes)
    nr_poza2 = random.randint(0,no_of_memes)
    poza1 = "/static/poze/memes/" + str(nr_poza1) + ".jpg"
    poza2 = "/static/poze/memes/" + str(nr_poza2) + ".jpg"
    if request.method == 'POST':
        poza1_scor, poza2_scor = map(float, citire_scor('scor.txt', nr_poza1, nr_poza2))
        if request.form.get('1') == '1':
            poza1_expected, poza2_expected = poza_expected(poza1_scor, poza2_scor)
            poza1_scornou = poza_scornou(poza1_scor, poza1_expected, 1)
            poza2_scornou = poza_scornou(poza2_scor, poza2_expected, 0)
            replace_line('scor.txt', nr_poza1, str(poza1_scornou)+'\n')               
            replace_line('scor.txt', nr_poza2, str(poza2_scornou)+'\n')         
        if request.form.get('2') == '2':
            poza1_expected, poza2_expected = poza_expected(poza1_scor, poza2_scor)
            poza1_scornou = poza_scornou(poza1_scor, poza1_expected, 0)
            poza2_scornou = poza_scornou(poza2_scor, poza2_expected, 1)
            replace_line('scor.txt', nr_poza1, str(poza1_scornou)+'\n')              
            replace_line('scor.txt', nr_poza2, str(poza2_scornou)+'\n') 

    poze_top_id = []
    v = top('scor.txt', 10)
    for i in range(len(v)):
        poze_top_id.append("/static/poze/memes/" + v[i] + ".jpg")
    
    return render_template("home.html", nr_poza1 = nr_poza1, nr_poza2 = nr_poza2,
                                     poza1 = poza1, poza2 = poza2, poze_top_id = poze_top_id)





if __name__ == '__main__':
        app.run(debug=True)