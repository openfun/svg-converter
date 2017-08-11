from django_cron import CronJobBase, Schedule
from converter.utils import CONVERTED_FILES_PREFIX

import tempfile
import os, glob


class PurgeFiles(CronJobBase):
    RUN_EVERY_MINS = 24*60 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'converter.purgefiles'    # a unique code

    def do(self):
        # Remove all temporary files
        for f in glob.glob( os.path.join(tempfile.gettempdir(), CONVERTED_FILES_PREFIX+"*") ):
            os.remove(f)
