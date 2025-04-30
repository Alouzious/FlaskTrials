from flask import render_template
from . import dashboard  

@dashboard.route('/dashboard')
def dashboard_page():

    return render_template('dashboard/dashboard.html')
