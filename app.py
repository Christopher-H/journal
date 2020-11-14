from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error
from db import dbconnection
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("welcome.html")


@app.route("/thoughts")
def thoughts():
    rows = findAllJournals()
    return render_template("journals.html", journals=rows)


@app.route("/writehere")
def writehere():
    return render_template("upload.html")


@app.route("/edit")
def edit():
    return render_template("edit.html")


@app.route("/results")
def results():
    return render_template("result.html")


@app.route("/new")
def newJournal():
    return render_template("newjournal.html")


@app.route("/addJournal", methods=['POST'])
def addJournal():
    msg = ""
    try:
        print("inside of addjournal")
        title = request.form['title']
        date = request.form['date']
        author = request.form['author']
        tag = request.form['tag']
        emotion = request.form['emotion']
        content = request.form['content']

        con = dbconnection()
        cur = con.cursor()
        cur.execute("INSERT INTO Journal(title, date, content, author, emotion, tag) VALUES(?, ?, ?, ?, ?, ?)",
                    (title, date, content, author, emotion, tag))
        print("about to commit")
        con.commit()
        msg = "Journal successfully saved"

    except Error as e:
        print("Error, can not upload" + e)
    finally:
        # cur.close()
        # con.close()
        return render_template("result.html", msg=msg)


@app.route("/editJournal/<int:id>")
def editJournal(id):
    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("select * from Journal where id = ?", (str(id),))
        row = cur.fetchone()
        print(row)
        if row:
            return render_template("edit.html", aJournal=row)
        else:
            msg = "Cannot find the journal with this id"
    except Error as e:
        print("There is an error" + e)
        msg = e
    finally:
        cur.close()
        con.close()


@app.route("/update", methods=["POST"])
def updateJournal():
    msg = ""
    try:
        _id = request.form['id']
        title = request.form['title']
        date = request.form['date']
        # author = request.form['author']
        tag = request.form['tag']
        emotion = request.form['emotion']
        content = request.form['content']
        print(_id, title, date, tag)

        con = dbconnection()
        cur = con.cursor()
        cur.execute("UPDATE Journal SET title = ?, date = ?, content = ?, emotion = ?, tag = ? WHERE id = ?",
                    (title, date, content, emotion, tag, _id))
        con.commit()
        msg = "Update Successful"
        return redirect("/thoughts")
    except Error as e:
        print("Error" + e)
        con.rollback()
        msg = "There is an error, rollback time."
    finally:
        cur.close()
        con.close()


@app.route("/view")
def viewJournal():
    return render_template("viewjournal.html")


# @app.route("/journals")
# This function is to test db connection
def findAllJournals():
    con = dbconnection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    return rows


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()


@app.route("/delete/<int:id>")
def deleteJournal(id):

    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("DELETE FROM Journal WHERE id= ?", (str(id),))
        con.commit()
        msg = "Journal deleted"
        return redirect("/thoughts")
    except Error as e:
        print("There is an error" + e)
        con.rollback()
        msg = "Error with deleting content"
    finally:
        cur.close()
        con.close()
