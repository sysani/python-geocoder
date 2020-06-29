from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
import pandas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success-table', methods=['POST'])
def success_table():
    if request.method=="POST":
        file=request.files['file']
        df=pandas.read_csv(file)
        return render_table(df)

def render_table(df):
    try:
        gc=Nominatim(user_agent="app.py")
        df['coordinates']=df['Address'].apply(gc.geocode)
        df['Latitude']=df['coordinates'].apply(lambda x: x.latitude if x != None else None)
        df['Longitude']=df['coordinates'].apply(lambda x: x.longitude if x != None else None)
        df=df.drop('coordinates',1)
        df.to_csv("uploads/geocoded.csv", index=None)
        return render_template("index.html", text=df.to_html(), btn="download.html")
    except:
        return render_template("index.html", text="Please enter a file with an address column")

@app.route('/download-file/')
def download():
    return send_file('uploads/geocoded.csv', attachment_filename='yourfile.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

'''
to run:
$ FLASK_APP=app.py flask run
'''
