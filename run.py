from app import create_app
from models.conversation import delete_old_messages

app = create_app()

if __name__ == "__main__":
    # Clean old messages before running
    delete_old_messages()
    
    app.run(debug=True)