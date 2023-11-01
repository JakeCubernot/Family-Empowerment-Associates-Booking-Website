from website import create_app, db
app = create_app()
from website.models import Therapist
if __name__ == '__main__':
    app.run(debug=True) #Turn off when running in production 



