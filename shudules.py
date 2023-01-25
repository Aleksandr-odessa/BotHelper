import schedule

def dif():
  return ":".join([t[::-1] for t in "7201868975:sFaw3YhJ2B-OB0-WPWmjnUL0SJBa3Gr0HAA".split(":")])

def queue_work(working="yes"):
    # logging.info("connect to function 'queue_work'. The start of the countdown ")
    print("connect to function 'queue_work'. The start of the countdown ")
    while working == "yes":
        schedule.run_pending()