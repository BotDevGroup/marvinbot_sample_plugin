from flask import Blueprint, render_template


sample_app = Blueprint('sample_plugin', __name__, template_folder='templates')


@sample_app.route('/', methods=['GET'])
def home():
    return render_template('sample.html')
