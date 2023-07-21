import subprocess


def executeJob(scriptName):
    impmodule = __import__(scriptName)
    impmodule.runJob()
    # subprocess.Popen(['python', scriptName])


executeJob("testJob")