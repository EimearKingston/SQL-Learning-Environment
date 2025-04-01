from flask_wtf import FlaskForm 
from wtforms import SelectField, StringField, PasswordField, IntegerField, SubmitField, FileField
from wtforms.validators import InputRequired, EqualTo 
# class QueryForm(FlaskForm):
#     query=StringField("Please enter a query: ", validators=[InputRequired()] )
#     submit=SubmitField("Submit") 

# class QueryForm(FlaskForm):
#     pass 


class QueryForm(FlaskForm):
        query = StringField("Enter your SQL Query:", render_kw={"class": "query"})
        submit = SubmitField("Submit", render_kw={"class": "submit"}) 

class LoginForm(QueryForm): 
    username=StringField("Please enter username:", validators=[InputRequired()] )
    password=PasswordField("Please enter password:", validators=[InputRequired()])
    submit=SubmitField("Submit") 

class SignForm(FlaskForm):
    username=StringField("Please enter a username:", validators=[InputRequired()] )
    password=PasswordField("Please enter a password:", validators=[InputRequired()])
    password_again=PasswordField("Confirm password:", validators=[InputRequired(), EqualTo("password")])
    submit=SubmitField("Submit") 

class UploadForm(FlaskForm): 
    workbook_name=StringField("Please enter workbook name:", validators=[InputRequired()] ) 
    database=FileField("Choose an .sqlite database file to upload (if necessary):") 
    existing_db = SelectField("Or select an existing database:", choices=[("Choose a database:", "")])
      
    question_file = FileField("Choose a question file to upload:", validators=[InputRequired()]) 
    solutions_file = FileField("Choose a solution file to upload:", validators=[InputRequired()])      
    submit = SubmitField("Upload")
   


   