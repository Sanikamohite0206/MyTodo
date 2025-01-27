from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:/Sanika/VIT_2024-27/II nd YEAR/Semester III/Python December 24/Flask/todo.db"

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)


# Define the database model for storing Todo items
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Primary key: serial number (auto-incremented)
    title = db.Column(db.String(200), nullable=False)  # Title of the Todo (max 200 characters)
    desc = db.Column(db.String(1000), nullable=False)  # Description of the Todo (max 1000 characters)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation, defaults to the current UTC time

    # String representation for debugging and logging purposes
    def __repr__(self) -> str:
        return f"{self.sno} {self.title}"
    
    

# Route for the home page ("/") which handles both GET and POST methods
@app.route("/", methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':  # Check if the request is POST
        # Retrieve the title and description from the form data
        title = request.form['title']
        desc = request.form['desc']

        # Create a new Todo object and add it to the database
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()  # Commit the changes to the database
        
    
    
    # Fetch all Todo items from the database to display on the page
    alltodo = Todo.query.all()
    
    # Render the template with the list of todos
    return render_template("index.html", allTodo=alltodo)



# Route to update a Todo item based on its serial number (sno)
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":  # Check if the request is POST
        # Retrieve the updated title and description from the form
        title = request.form['title']
        desc = request.form['desc']

        # Fetch the Todo item to update from the database
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title  # Update the title
        todo.desc = desc  # Update the description
        db.session.add(todo)  # Add the updated object to the session
        db.session.commit()  # Commit the changes to the database
        
        return redirect('/')  # Redirect to the home page
    
    # Fetch the Todo item to display in the update form
    utodo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=utodo)



# Route to delete a Todo item based on its serial number (sno)
@app.route("/delete/<int:sno>", methods=['GET'])
def delete(sno):
    # Fetch the Todo item to delete from the database
    dtodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(dtodo)  # Delete the item
    db.session.commit()  # Commit the changes to the database
    return redirect("/")  # Redirect to the home page


@app.route("/about/",methods=['GET','POST'])
def about():
    return render_template("about.html")


# Main block to run the app
if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode for easier troubleshooting
