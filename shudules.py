import schedule

def queue_work(working="yes"):
    # logging.info("connect to function 'queue_work'. The start of the countdown ")
    print("connect to function 'queue_work'. The start of the countdown ")
    while working == "yes":
        schedule.run_pending()
