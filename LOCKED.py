import GUI
import background
import threading


t = threading.Thread(target=background.start, args=())
t.daemon = True
t.start()
GUI.main()