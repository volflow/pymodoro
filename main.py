import rumps
import time
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve

rumps.debug_mode(True)

TIME_INTERVAL = 25*60

def timez():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())


class TimerApp(object):
    def __init__(self, timer_interval=1):
        self.timer = rumps.Timer(self.on_tick, 1)
        self.timer.stop()  # timer running when initialized
        self.timer.count = 0
        self.app = rumps.App('Pymodoro')
        self.start_pause_button = rumps.MenuItem(title='Start timer',
                                                 callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title='Stop timer',
                                                callback=self.stop_timer)
        self.app.menu = [self.start_pause_button,
                         self.stop_button]
        self.app.icon = 'icons/tomato.png'

    def run(self):
        self.app.run()

    def start_timer(self, sender):
        # print(sender.title)

        if sender.title in ['Start timer', 'Continue timer']:

            if sender.title == 'Start timer':
                # reset timer & set stop time
                self.timer.count = 0
                self.timer.end = TIME_INTERVAL

            # change title of MenuItem from 'Start timer' to 'Pause timer'
            sender.title = 'Pause timer'
            self.app.icon = 'icons/hour_glass_going.png'

            # lift off! start the timer
            self.timer.start()
        else:  # 'Pause Timer'
            # print('test')
            sender.title = 'Continue timer'
            self.app.icon = 'icons/hour_glass_idle.png'
            self.timer.stop()

    def on_tick(self, sender):
        #print('%r %r' % (sender, timez()))
        try:
            # print(sender.count)
            time_left = sender.end - sender.count
            # handle minute and second counter if positive/negative time left
            mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
            secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
            print(mins, secs)
            if mins == 0 and time_left < 0:
                # add minus sign if between -1 and -59 seconds
                self.app.title = '-{:2d}:{:02d}'.format(mins, secs)
            else:
                self.app.title = '{:2d}:{:02d}'.format(mins, secs)

            sender.count += 1
            if sender.count == sender.end:
                rumps.notification(title='Time is up! Take a break :)',
                                   subtitle='PyModoro',
                                   message='')
                print('stopping timer')
                # stop_timer()
        except Exception as ex:
            print('Did not work', ex)

    def stop_timer(self, sender=None):
        print('Called right fct')
        self.timer.stop()
        self.timer.count = 0
        self.app.title = None
        self.app.icon = 'icons/tomato.png'
        self.start_pause_button.title = 'Start timer'
        #app.menu._menu[0].title = 'Start timer'


if __name__ == '__main__':
    app = TimerApp(timer_interval=1)
    app.run()
