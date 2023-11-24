from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, URLField, TimeField
from wtforms.validators import DataRequired, InputRequired, URL
import csv
import pandas as pd

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# Form class for café details
class CafeForm(FlaskForm):
    # Form fields with validators
    cafe = StringField('Cafe name', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee', choices=['Select', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'],
                                validators=[InputRequired()])
    wifi_quality = SelectField(label='WiFi Quality',
                               choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
                               validators=[InputRequired()])
    power_quality = SelectField(label='Power Quality',
                                choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
                                validators=[InputRequired()])
    location_url = URLField(label='Location URL',
                            validators=[URL()])
    open_time = TimeField(label='Open Time',
                          validators=[InputRequired()])
    close_time = TimeField(label='Closing Time',
                           validators=[InputRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    if form.validate_on_submit():
        # Retrieve form data on successful submission
        cafe_name = form.cafe.data
        open_time = form.open_time.data
        closing_time = form.close_time.data
        location_url = form.location_url.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_quality.data
        power_rating = form.power_quality.data

        # Create a DataFrame and append data to a CSV file
        data = {
            'Cafe Name': [cafe_name],
            'Location': [location_url],
            'Open': [open_time],
            'Close': [closing_time],
            'Coffee': [coffee_rating],
            'Wifi': [wifi_rating],
            'Power': [power_rating],
        }

        df = pd.DataFrame(data)
        df.to_csv('cafe-data.csv', mode='a', index=False, header=False)

        return render_template('add.html', form=form)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # Read café data from the CSV file
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
