import sys, os




print(os.getcwd())
print(sys.executable)
print(sys.argv)
# 
# print(os.path.dirname(sys.executable))
# os.system("pause")

print("-----------------------------------test-----------------------------------")
print(os.path.abspath(os.path.join(__file__, '..', 'static')))