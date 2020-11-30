from gpiozero import Button, LED
from time import sleep, clock
import multiprocessing
import logging


# main class to control raspberry pi PINS, log activity
class raspModel():
    def __init__(self, settings, bot):
        self.doorBell_watcher = Button(settings['doorBell_watcherPIN'],
                                       pull_up=True, bounce_time=0.1)  # pin to observe for incoming guest
        self.bell = LED(settings['bellPIN'])  # pin to control physical bell
        self.door = LED(settings['doorPIN'])  # pin to control door opening
        self.settings = settings
        self.bot = bot
        self.openCode = 0  # counter of doorbell press
        self.logger = logging.getLogger('main_log')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('log.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def getBell(self):
        return self.bell.value

    # function to enable physical bell
    def ring(self):
        self.bell.on()
        sleep(1)
        self.logger.debug('RING')

    def ringoff(self):
        self.bell.off()

    def logMessage(self, message):
        self.logger.debug(message)

    # function to notify users (facebook)
    def notify(self):
        try:
            self.bot.send_text_message(self.settings['ID1'], 'RING')
            self.bot.send_text_message(self.settings['ID2'], 'RING')
            self.logger.debug('Notify fb')
        except:
            self.logger.debug('Could not notify')

    def getringRealBell(self):
        return self.ringRealBell

    def setRingRealBell(self, value):
        self.ringRealBell = value

    # function to open doors
    def openDoors(self):
        self.door.on()
        sleep(3)
        self.door.off()
        self.settings['openDoor'] = 0
        self.logger.debug('open doors')


# class with separate thread to wait for doorbell press and behave by press time and pattern
class door_watcher(multiprocessing.Process):
    def __init__(self, settings, rasp):
        multiprocessing.Process.__init__(self)
        self.settings = settings
        self.rasp = rasp
        self.openCode = 0
        self.timeOn = 0
        self.timeOf = 0

    def run(self):
        while True:
            sleep(0.1)
            if self.rasp.doorBell_watcher.is_pressed:
                self.timeOn = clock()
                if self.timeOn-self.timeOf > 2:
                    self.openCode = 0
                while self.rasp.doorBell_watcher.is_pressed:
                    if clock() - self.timeOn > self.settings['delayTime']:
                        self.openCode = 0
                        self.rasp.notify()
                        if self.settings['ringRealBell'] == 1:
                            self.rasp.ring()
                self.rasp.ringoff()
                self.timeOf = clock()
                if self.timeOf - self.timeOn > 2:  # set to zero if interval between presses to long
                    self.openCode = 0
                if self.timeOf - self.timeOn < self.settings['openCodeTime']:
                    if self.timeOf - self.timeOn > 0.1:
                        self.openCode = self.openCode + 1
                else:
                    self.openCode = 0
                if self.openCode > 2:
                    self.rasp.openDoors()
                    self.openCode = 0
                    self.rasp.logger.debug('open from combination (openCode)')
                message = self.timeOf - self.timeOn
                self.rasp.logMessage(message.__str__())
