import time

class InputDialogHandler:
    def __init__(self, session,user):
        self.session = session
        self.tablet_service = session.service("ALTabletService")
        self.signal_id = None
        self.user = user
        self.counter = 0

    def show_input_dialog(self, title, ok_text, cancel_text):
        self.tablet_service.showInputTextDialog(title, ok_text, cancel_text)
        self.signal_id = self.tablet_service.onInputText.connect(self.on_input_text)


    def on_input_text(self, button_id, input_text):
        if button_id == 1:
            print("'OK' button is pressed.")
            print("Input text: " + input_text)
            if self.counter == 0:
                self.user.name = input_text
                self.counter = self.counter+1

            elif self.counter == 1:
                self.user.surname = input_text
                self.counter = self.counter+1

            elif self.counter == 2:
                self.user.age = int(input_text)
                self.counter = self.counter+1
        else:
            exit(1)

        self.tablet_service.onInputText.disconnect(self.signal_id)