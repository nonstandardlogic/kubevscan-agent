import subprocess

list_files = subprocess.Popen(['ls', '-l', '.'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
stdout,stderr = list_files.communicate()
print("stdout was ")
print(stdout)
print("stderr was ")
print(stderr)
print("exit code was: %d" % list_files.returncode)

