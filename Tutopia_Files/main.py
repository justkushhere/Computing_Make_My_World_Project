from flask import Flask, render_template, request,redirect, url_for
import sqlite3
connection = sqlite3.connect("Tutors.db")
try:
    connection.execute("CREATE TABLE Tutors(Name,Email,Subject,Experience)")
except:
    print("table exists!")

app = Flask(__name__)

def x_match(basis,Tutors,term):#basis is the index of the item in the tuple that we are matching
    output = []
    for tutor in Tutors:
        if tutor[basis] == term:
            output.append(tutor)
            print("ADDED",tutor)
        else:
            print("NOT ADDED")
    return output

#Fetching Tutors
def Tutors_Default(): #All, without sorting, without grouping
    connection = sqlite3.connect("Tutors.db")

    cursor = connection.execute("SELECT * FROM Tutors")
    Tutors = []
    for row in cursor:
        Tutors.append(row)
    return Tutors

def Tutors_SORT_Exp(): #All, Sorted by Experience
    Tutors = Tutors_Default()
    if len(Tutors) == 0:
        return Tutors
    else:
        Tutors_Sorted = sorted(Tutors, key=lambda tutor: tutor[3], reverse=True)
    return  Tutors_Sorted

    '''
    connection = sqlite3.connect("Tutors.db")

    cursor = connection.execute("SELECT * FROM Tutors ORDER BY Experience DESC")
    Tutors = []
    for row in cursor:
        Tutors.append(row)
    return Tutors
    '''

def Tutors_GRPBY_SBJ(): #All, Sorted by Subject
    Tutors = Tutors_Default()
    if len(Tutors) == 0:
        return Tutors
    else:
        Tutors_Sorted = sorted(Tutors, key=lambda tutor: tutor[2])
    return  Tutors_Sorted
    

def Tutors_Search(Search_Term): #Selective, Match with search term
    Tutors = Tutors_Default()
    print(Tutors)
    subject_filter = lambda Tutors, Search_Term:  any(Tutor[2] == Search_Term for Tutor in Tutors)
    #subject_match = list(filter(lambda x: subject_filter(x,Search_Term),Tutors))
    subject_match = x_match(2,Tutors=Tutors,term=Search_Term)
    print(subject_match)

    name_filter = lambda Tutors, Search_Term:  any(Tutor[0] == Search_Term for Tutor in Tutors)
    #name_match = list(filter(lambda x: name_filter(Tutors,Search_Term)))
    name_match = x_match(0,Tutors=Tutors,term=Search_Term)

    email_filter = lambda Tutors, Search_Term:  any(Tutor[1] == Search_Term for Tutor in Tutors)
    #email_match = list(filter(lambda x: email_filter(Tutors,Search_Term)))
    email_match = x_match(1,Tutors=Tutors,term=Search_Term)

    Tutors = []
    Tutors.extend(subject_match)
    Tutors.extend(name_match)
    Tutors.extend(email_match)
    print(Tutors,"OUTPUTLIST")
    return Tutors
    '''
    connection = sqlite3.connect("Tutors.db")
    Tutors = [
    cursor1 = connection.execute("SELECT * FROM Tutors")
    for row in cursor1:
        print(row)
        if row[2] == Search_Term:
            Tutors.append(row)
        elif row[0] == Search_Term:
            Tutors.append(row)
        #elif row[1] == Search_Term:
        '''



@app.route('/')
def tutor_form():
    return render_template('index.html')

@app.route('/educator')
def educator():
    return render_template("Tutopia_Educator.html")

@app.route('/student')
def student():
    Tutors = Tutors_Default()
    return render_template("Tutopia_Student.html", Tutors = Tutors)

@app.route('/student/sort_by_exprience')
def student_SORT_Exp():
    Tutors = Tutors_SORT_Exp()
    return render_template("Tutopia_Student.html", Tutors = Tutors)

@app.route('/student/group_by_subject')
def student_GRPBY_SBJ(Tutors = None):
    if Tutors == None:
        Tutors = Tutors_GRPBY_SBJ()
    
    return render_template("Tutopia_Student.html", Tutors = Tutors)

@app.route('/student/search?query=<s>', methods = ['GET','POST'])
def student_SEARCH(s):
    Tutors = Tutors_Search(s)
    return render_template("Tutopia_Student.html", Tutors = Tutors)

@app.route('/student/search?', methods = ['GET','POST'])
def student_SEARCH_process():
    query = request.form['search_query']
    if query == "":
        query = "<BlankQuery>"
    return redirect(url_for('student_SEARCH',s=query))


@app.route("/sort")
def sort():
    print("Sorting")
    return render_template("Tutopia_Educator.html")



@app.route('/submit', methods=['POST'])
def submit_tutor_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        experience = request.form['experience']
        
        
        print("Name:", name)
        print("Email:", email)
        print("Subject:", subject)
        print("Experience:", experience)

        connection = sqlite3.connect("Tutors.db")

        connection.execute("INSERT INTO Tutors(Name,Email,Subject,Experience) VALUES(?,?,?,?)",(name,email,subject,experience))
        connection.commit()
        return 'Form submitted successfully!'
    else:
        return render_template("Tutopia_Student.html")

if __name__ == '__main__':
    app.run(debug=True)

connection.commit()
connection.close()