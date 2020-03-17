import docker
import os
import time
import re
import subprocess

# by Justin Hagerty

#in case this script fails to finish you can execute stopAll to clear out all docker containers but its not written yet.


client = docker.from_env()

def upload(localFile, targetDir, targetContainer):
    os.path.dirname(os.path.realpath(__file__))
    shellStream = subprocess.Popen("docker cp " + localFile + " " + targetContainer.id + ":" + targetDir)
    while (shellStream.poll() == None):
        print("Copying the file - the copy process is still runnining...")
        time.sleep(1)
    for y in range(0, 15):
        for x in targetContainer.diff():
            if (targetDir + localFile == x["Path"]):
                return True
        print("checking upload...")
        # Dont have a good way to check to see if it is complete yet - need to adjust timeout to ensure that it allows for upload to complete - I was working on a diff function to see if it uplaoded right.
        time.sleep(0.25)
        if (y > 10):
            print("upload failed for one reason or another....")
            return False

pythonContainer = client.containers.run('python', command="tail -f /dev/null", detach=True)
print(pythonContainer.short_id)
if (upload("test.py", "/", pythonContainer)):
    print(pythonContainer.exec_run(cmd="/bin/sh -c 'python /test.py'").output)
pythonContainer.stop()


