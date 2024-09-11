import qi
import sys
from input_dialog_handler import InputDialogHandler
from user import User
from pepper_controller import PepperController
import database

def main(session):
    controller = PepperController(session)
    controller.initialize()
    #controller.registerUserPositiveBehaviour()
    controller.registerUserNegativeBehaviour()
    raw_input("Press Enter to continue...")
    #controller.falseBeliefsTaskPositive()
    controller.falseBeliefsTaskNegative()
    
if __name__ == "__main__":
    try:
        connection_url = "tcp://192.168.2.67:9559"  # Replace with your robot's IP and port
        app = qi.Application(url=connection_url)
        app.start()
        database.createDatabase()
    except RuntimeError:
        print("Can't connect to Naoqi.")
        sys.exit(1)
    main(app.session)   
    
