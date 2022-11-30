import subprocess
import shlex


output = subprocess.check_output(shlex.split("sleep 5 ping ya.ru"))
print(output.decode())
