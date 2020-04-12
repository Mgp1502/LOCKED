import GUI2
import background
import threading


t = threading.Thread(target=background.start, args=())
t.daemon = True
t.start()
GUI2.main()