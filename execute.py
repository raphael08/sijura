import scheduler_jobs
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from pytz import utc
from scheduler_jobs import *
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)

scheduler.add_job(scheduler_jobs.sendTxt, 'interval', seconds=3600)
scheduler.add_job(scheduler_jobs.birthday, 'interval', seconds=60)


try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
