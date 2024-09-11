import qi
def main(session):
    autonomous_life_proxy = session.service("ALAutonomousLife")
    autonomous_life_proxy.setState("disabled")

if __name__ == "__main__":
    try:
        connection_url = "tcp://192.168.2.67:9559"  # Replace with your robot's IP and port
        app = qi.Application(url=connection_url)
        app.start()
    except RuntimeError:
        print("Can't connect to Naoqi.")
        sys.exit(1)
    main(app.session)   