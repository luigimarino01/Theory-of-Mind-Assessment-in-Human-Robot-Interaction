import time
from input_dialog_handler import InputDialogHandler
from user import User
import database
from PIL import Image
import os
import cv2
import numpy as np
import math


class PepperController:
    def __init__(self, session):
        self.session = session
        self.tablet_service = session.service("ALTabletService")
        self.user = User()  
        self.initialized = False
       
    def initialize(self):
        if not self.initialized:
            self.tablet_service = self.session.service("ALTabletService")
            self.dialog_service = self.session.service("ALDialog")
            self.text_to_speech = self.session.service("ALTextToSpeech")
            self.posture_proxy = self.session.service("ALRobotPosture")
            self.memory_proxy = self.session.service("ALMemory")
            self.motion_proxy = self.session.service("ALMotion")
            self.speech_detection_proxy = self.session.service("ALSpeechRecognition")
            self.photo_capture_proxy = self.session.service("ALPhotoCapture")
            self.emotion_analysis_proxy = self.session.service("ALVoiceEmotionAnalysis")
            self.animated_speech_proxy = self.session.service("ALAnimatedSpeech")
            self.autonomous_life_proxy = self.session.service("ALAutonomousLife")
            self.led_proxy = self.session.service("ALLeds")
            self.speech_detection_proxy.setLanguage("English")
            self.dialog_service.setLanguage("English")
            self.text_to_speech.setParameter("pitchShift", 1.2)
            self.text_to_speech.setParameter("speed", 100)
            self.text_to_speech.setLanguage("Italian")
            self.initialized = True
            
        

        else:
            print("Services are already initialized.")

    def reset_position(self):
        self.posture_proxy.goToPosture("Stand", 1.0)

    def say_text(self, text):
        self.text_to_speech.say(text)

    def say_animated_text(self, text):
        self.animated_speech_proxy.say(text)

    def headMove(self):
        head_joints = ["HeadYaw", "HeadPitch"]
        stiffness = 1.0  
        self.motion_proxy.stiffnessInterpolation(head_joints, stiffness, 6.0)
        
    def moveHeadWithAngle(self):
        self.motion_proxy.setAngles(["HeadPitch", "HeadYaw"], [math.radians(13.2), math.radians(-13.2)], 1.0)
    
    def moveBodyWithAngle(self, value):
        self.motion_proxy.setAngles(["HipPitch"], [value], 1.0)
     
    def pointBall(self):
        shoulder_pitch_angle = math.radians(20.4) 
        elbow_yaw_angle = math.radians(119.5)  
        elbow_roll_angle = math.radians(1.2)
        wrist_yaw_angle = math.radians(17.7)  
        hand_angle = 1.0  
        shoulder_roll_angle = math.radians(-0.5)
        angles = [shoulder_pitch_angle, elbow_yaw_angle, wrist_yaw_angle, hand_angle, elbow_roll_angle, shoulder_roll_angle]
        names = ["RShoulderPitch", "RElbowYaw", "RWristYaw", "RHand", "RElbowRoll", "RShoulderRoll"]
        self.motion_proxy.setAngles(names, angles, 0.2)


        head_pitch = math.radians(5.2)
        head_yaw = math.radians(-10.5)
        angles_head = [head_pitch, head_yaw]
        names_head = ["HeadPitch", "HeadYaw"]
        self.motion_proxy.setAngles(names_head, angles_head, 0.2)

    def pointBox(self):
        shoulder_pitch_angle = math.radians(0.7)  
        elbow_yaw_angle = math.radians(119.5)  
        elbow_roll_angle = math.radians(1.2)
        wrist_yaw_angle = math.radians(17.7)  
        hand_angle = 1.0  
        shoulder_roll_angle = math.radians(-13)

        angles = [shoulder_pitch_angle, elbow_yaw_angle, wrist_yaw_angle, hand_angle, elbow_roll_angle, shoulder_roll_angle]
        names = ["RShoulderPitch", "RElbowYaw", "RWristYaw", "RHand", "RElbowRoll", "RShoulderRoll"]
        self.motion_proxy.setAngles(names, angles, 0.2)

        head_pitch = math.radians(5.2)
        head_yaw = math.radians(-10.5)
        angles_head = [head_pitch, head_yaw]
        names_head = ["HeadPitch", "HeadYaw"]
        self.motion_proxy.setAngles(names_head, angles_head, 0.2)

    def turn(self, value):
        angle = math.radians(value)
        while True:
            print("imturning")
            old_angle = self.motion_proxy.getRobotPosition(False)[2]
            result = self.motion_proxy.moveTo(0.0, 0.0, angle)
            print("Result: " + str(result))
            print("Angle: " + str(angle))
            new_angle = self.motion_proxy.getRobotPosition(False)[2]
            print("Robot angle: " + str(new_angle))
            if result and old_angle != new_angle:
                break
            
    def registerUserPositiveBehaviour(self):
        self.reset_position()
        self.led_proxy.fadeRGB("FaceLeds","green", 1)
        self.text_to_speech.setParameter("pitchShift", 1.2)
        self.text_to_speech.setParameter("speed", 110)
        print("Collecting user data...")
        self.say_animated_text("Ciao, mi chiamo Pepper, piacere di conoscerti.")
        self.say_animated_text("Che bello vederti!")
        self.say_animated_text("Mi dispiace doverti disturbare , ma prima di iniziare dovresti compilare un form sul mio tablet, per piacere.")
        input_dialog_handler = InputDialogHandler(self.session, self.user)
        time.sleep(2)
        input_dialog_handler.show_input_dialog("Name", "OK", "Cancel")
        while self.user.name is None:
            time.sleep(1)
        self.say_animated_text("Che bel nome!")
        input_dialog_handler.show_input_dialog("Surname", "OK","Cancel")
        while self.user.surname is None:
            time.sleep(1)
        self.say_animated_text("Adesso per piacere come ultimo form.")
        input_dialog_handler.show_input_dialog("Age", "OK", "Cancel")
        while self.user.age is None:
            time.sleep(1)

        database.insertUser(self.user.name, self.user.surname,self.user.age, "Interactive")
        self.say_animated_text("Grazie per aver contribuito!")
        self.say_animated_text(self.user.name)
        self.say_animated_text("Ho degli assistenti qui con me, ti aiuteranno per i prossimi passi.")
        time.sleep(1)
        self.turn(90)
        time.sleep(1)

    def registerUserNegativeBehaviour(self):
        self.reset_position()
        self.text_to_speech.setParameter("pitchShift", 0)
        self.text_to_speech.setParameter("speed", 75)
        self.moveHeadWithAngle()
        self.moveBodyWithAngle(0.0)
        self.led_proxy.fadeRGB("FaceLeds","red", 1)
        print("Collecting user data...")
        self.say_text("Ciao, compila il form sul mio tablet.")
        self.say_text("Ci servono questi dati per i nostri studi.")     
        input_dialog_handler = InputDialogHandler(self.session, self.user)
        self.say_text("Inserisci il tuo nome.")
        input_dialog_handler.show_input_dialog("Name", "OK", "Cancel")
        while self.user.name is None:
            time.sleep(1)
        self.say_text("Inserisci il tuo cognome.")
        input_dialog_handler.show_input_dialog("Surname", "OK","Cancel")
        while self.user.surname is None:
            time.sleep(1)
        input_dialog_handler.show_input_dialog("Age", "OK", "Cancel")
        while self.user.age is None:
            time.sleep(1)
        self.say_text("Utente creato.")
        self.say_text("Qualcuno adesso ti aiutera a procedere.")
        database.insertUser(self.user.name, self.user.surname,self.user.age, "Passive")
        self.turn(90)

    def falseBeliefsTaskPositive(self):
        
        self.reset_position()
        self.moveHeadWithAngle()
        self.say_animated_text("Hey, sei ancora tu.")
        self.say_animated_text("Guarda questa pallina, passo intere ore a giocarci.")
        self.moveHeadWithAngle
        self.pointBall()
        self.moveHeadWithAngle()
        time.sleep(2)
        self.say_animated_text("Potresti per piacere metterla nella scatola rossa e chiudere entrambe le scatole??")
        self.pointBox()
        self.moveHeadWithAngle()
        raw_input("Press enter when the ball is in the box")
        self.say_animated_text("Grazie mille!")
        self.say_animated_text("Oh, mi stanno chiamando, scusami un attimo.")
        time.sleep(1)
        self.reset_position()
        time.sleep(3)
        self.turn(-180)
        time.sleep(1)
        self.text_to_speech.setParameter("pitchShift", 2.0)
        self.text_to_speech.setParameter("speed", 200)
        self.say_text("Pronto??")
        time.sleep(3)
        self.say_text("Hi, it's good to hear you but I am busy right now")
        self.say_text("bhvfiopwlskdjchgdbwnksdodiugqoal?")
        self.say_text("ajcoehwpaoes")        
        self.say_text("I will call you later, alright?")
        raw_input("Press enter when the ball has been switched")
        self.say_text("Ciao ciao.")
        time.sleep(3)
        self.turn(180)
        time.sleep(1)
        self.text_to_speech.setParameter("pitchShift", 1.2)
        self.text_to_speech.setParameter("speed", 100)
        self.say_animated_text("Perdonami ancora una volta, dovevo rispondere.")
        self.say_animated_text("Grazie per aver partecipato al primo test!")
        self.moveHeadWithAngle()
        time.sleep(1)
        self.turn(-90)
        time.sleep(1)

    
        raw_input("Start second test")


        self.turn(90)
        self.say_animated_text("Hey, sei ancora tu.")
        self.say_animated_text("Guarda questa pallina, passo intere ore a giocarci.")
        self.pointBall()
        time.sleep(2)
        self.say_animated_text("Potresti per piacere metterla nella scatola rossa e chiudere entrambe le scatole?")
        self.pointBox()
        raw_input("Press when user inserted the ball")
        self.say_animated_text("Grazie mille!")
        self.moveHeadWithAngle()
        raw_input("Press when ball switched!")
        self.say_animated_text("Adesso vado a giocare con la pallina, grazie per aver partecipato al test.")
        self.turn(-90)

    def falseBeliefsTaskNegative(self):
        self.say_text("Questa e la mia pallina, mettila nella scatola rossa.")
        self.say_text("Chiudi poi entrambe le scatole.")
        raw_input("Press when user inserted the ball.")
        self.turn(-180)
        raw_input("Press when ball switched.")
        self.turn(180)
        self.say_text("Bene, adesso vado a giocare con la mia pallina.")
        self.turn(-90)
        raw_input("Press to start second test.")
        self.turn(90)
        self.say_text("Questa e la mia pallina, mettila nella scatola rossa.")
        self.say_text("Chiudi poi entrambe le scatole.")
        raw_input("Press when user inserted the ball.")
        self.say_text("Test terminato.")
        self.turn(-90)

        pass
