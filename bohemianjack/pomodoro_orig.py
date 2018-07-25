# Module imports for timer

import winsound
from datetime import datetime
from time import sleep
from sys import stdout

def get_time():
    """Gives the current time when function is called
    """
    
    return datetime.now()


def sound_wave():
    """Windows soundwaves to inform the user of timers going off
    """
    
    return ['C:/Windows/media/Speech On.wav',  # break countdown chime
            'C:/Windows/media/Speech Off',  # break complete chime
            'C:/Windows/media/Windows Unlock'  # switch work/break chime
            ]


def pomodoro_timer_work(check_mark=1, work_time=(60 * 25)):
    """"Actual Pomodoro Timer. Counts down from 25 minutes. Once it reaches
        less than 30 seconds, it gives the user a warning. Once it reaches
        5 seconds, it chimes each second, letting the user know it's time
        to work again.
    """
    print('CHECKMARK #:', check_mark), winsound.PlaySound(sound_wave()[2], winsound.SND_FILENAME)
    print('\rThe current time is: ', get_time().strftime('%I:%M %p'), end='\n')
    print('\r'+'Work Time! The timer is set for 25 minutes!',
          'You\'ll hear a beep when you have 30 seconds left before your break.', end='')
    sleep(work_time - 30)
    print('\r'+'Get Ready for your break! 30 seconds left.', end='')
    winsound.PlaySound(sound_wave()[1], winsound.SND_FILENAME)
    sleep(30)
    for i in range(5, 0, -1):
        print(f'\rBreak will start in {int(i)} second(s).', end=''),
        winsound.PlaySound(sound_wave()[1], winsound.SND_FILENAME)
    stdout.flush()
    print(f'\r'+'Work session #{int(check_mark)} complete!', end='\n\n'),
    winsound.PlaySound(sound_wave()[0], winsound.SND_FILENAME)
    return


def pomodoro_timer_break(check_mark=1, break_time=(60 * 5)):
    """Break timer. Gives a 5 minute break by default.
    """
    
    print('BREAK #:', check_mark), winsound.PlaySound(sound_wave()[2], winsound.SND_FILENAME)
    print('\rThe current time is: ', get_time().strftime('%I:%M %p'), end='\n')
    print(f'\rBreak Time! you have a {int(break_time/60)} minute break. The time will beep when you' \
          + ' have 10 seconds of your break left :)', end='')
    sleep(break_time)
    for i in range(10, -1, -1):
        print(f'\rBegin working in {str(i)} second(s).', end=''),
        winsound.PlaySound(sound_wave()[1], winsound.SND_FILENAME)
    stdout.flush()
    print(f'\rBreak session #{int(check_mark)} complete!', end='\n\n'),
    winsound.PlaySound(sound_wave()[0], winsound.SND_FILENAME)
    return


def info():
    explanation = 'A pomodoro timer is, simply put, an interval timer. You work in 25 minute sessions, followed by',
def main():
    """Main Function. Gives a menu of options, and has catches in case something
    is incorrectly inputed. It'll iterate the actual pomodoro timer and
    break functions until they meet the generally accepted intervals of
    a Pomodoro work session.
    """
    
    print('This is a pomodoro timer. It is a great way to take incremental breaks so you don\'t burn yourself out!')
    while True:
        try:
            print('Please choose from the following options: \n',
                  '\t1) Pomodoro timer instructions. \n',
                  '\t2) Run the pomodoro timer. \n',
                  '\t3) Exit the program.\n')
            menu_choice = int(input())
            if menu_choice == 1:
                print(info())
            elif menu_choice == 2:
                break_counter = 0
                print('Starting Pomodoro timer')
                sleep(1)
                for i in range(3):
                    pomodoro_timer_work(check_mark=i + 1)
                    if break_counter != 3:
                        pomodoro_timer_break(check_mark=i + 1)
                        break_counter += 1
                    else:
                        pomodoro_timer_break(check_mark=i + 1, break_time=(60 * 15))
                pomodoro_timer_work(check_mark=4)
                go_again = input('Do you want to start the timer again? (y/n): ')
                if go_again.lower() in ['y', 'yes', 'yep']:
                    continue
                else:
                    print('Goodbye!')
                    break

            elif menu_choice == 3:
                print('Goodbye!')
                break
            else:
                print('Looks like you mistyped... here, try again.\n')
                continue
        except ValueError:
            print('Looks like you mistyped... here, try again.\n')
            continue


if __name__ == '__main__':
    pomodoro_timer_break(break_time=30)
    main()