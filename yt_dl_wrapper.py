import subprocess, string

command = "youtube-dl --skip-download --get-title --get-id --get-duration --max-downloads 10 https://www.youtube.com/results?search_query=work+rihanna"
process = subprocess.Popen(command, stdout=subprocess.PIPE ,shell=True)
(output, error) = process.communicate()
output = output.rstrip('\n')

lines = string.split(output, '\n')

names = []
ids = []
times = []

for i in range(0,len(lines),3):
    names.append(lines[i])
    ids.append(lines[i+1])
    times.append(lines[i+2])

for i in range(0,len(names)):
    print "[", i, "] - ", names[i], times[i]

user_response = raw_input('Select your choice: ')

print ids[int(user_response)]
