from flask import Flask, request, render_template, redirect, url_for

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_tup = hackbright.get_grades_by_github(github)
    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           project_tup=project_tup)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/project-search")
def get_project_form():
    """Show form for searching for a project"""

    return render_template("project_search.html")


@app.route("/project")
def show_project_info():

    title = request.args.get("title")
    title, description, max_grade = hackbright.get_project_by_title(title)
    info_tup = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", title=title,
                           description=description, max_grade=max_grade,
                           info_tup=info_tup)


@app.route("/student-add", methods=['GET', 'POST'])
def student_add():
    """Add a student"""

    if request.method == 'GET':
        return render_template("student_add.html")

    elif request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        github = request.form.get('username')

        hackbright.make_new_student(fname, lname, github)

        return redirect(url_for("display_info", github=github))


@app.route("/success")
def display_info():
    """Displays confirmation of student add and link to student info page"""

    github = request.args.get('github')

    return render_template("confirmation.html", github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
