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

def on_tick(sender):
    #print('%r %r' % (sender, timez()))
    try:
        #print(sender.count)
        time_left = sender.end-sender.count
        app.title = '{:2d}:{:02d}'.format(time_left//60,time_left%60)

        sender.count += 1
        if sender.count > sender.end:
            stop_timer()
    except Exception as ex:
        print('Did not work', ex)

def start_timer(sender):
    #print(sender.title)

    if sender.title in ['Start timer','Continue timer']:
        sender.title = 'Pause timer'
        app.icon = 'icons/hour_glass_going.png'
        global_namespace_timer.start()
        #print(global_namespace_timer.is_alive())
    else:
        #print('test')
        sender.title = 'Continue timer'
        app.icon = 'icons/hour_glass_idle.png'
        global_namespace_timer.stop()


@rumps.clicked('Stop timer')
def stop_timer(_):
    global_namespace_timer.stop()
    global_namespace_timer.count = 0
    app.title = None
    app.icon = 'icons/tomato.png'
    start_pause_button.title = 'Start timer'
    #app.menu._menu[0].title = 'Start timer'


if __name__ == '__main__':
    global_namespace_timer = rumps.Timer(on_tick, 1)
    global_namespace_timer.stop()
    print(global_namespace_timer.is_alive())
    global_namespace_timer.end = TIME_INTERVAL
    global_namespace_timer.count = 0
    app = rumps.App('Pymer')

    start_pause_button = rumps.MenuItem(title='Start timer',callback=start_timer)
    app.menu = [start_pause_button]
    app.icon = 'icons/tomato.png'
    app.run()
    global_namespace_timer.stop()
