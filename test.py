import sys, os, time




print(os.getcwd())
print(sys.executable)
print(sys.argv)
print(os.path.splitext(sys.executable)) 
# print(os.path.dirname(sys.executable))
# os.system("pause")


print("-----------------------------------test-----------------------------------")
# sys.exit(0)
# os.system("exit")


print(" "*100, '-')
print("█"*100, '-')
percent= 100
print(f'下載中… {percent:05.2f}%', '█'*(int(percent)), ' '*(100-int(percent)), end='\r')

for i in range(4):
    sys.stdout.write("\r" + ("."*i*10))
    sys.stdout.flush()
    if i == 3:
        sys.stdout.write("\r\033[K")
    time.sleep(1.5)