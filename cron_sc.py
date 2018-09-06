from crontab import CronTab

my_cron = CronTab(user='USERNAME')
job = my_cron.new(command='python task.py')
job.minute.every(1)

my_cron.write()
