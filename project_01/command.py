import sys
import resource


method = str(sys.argv[1])
my_input = tuple(int(n) for n in sys.argv[2].split(','))

print(method)
print(my_input)
print('Memory usage: {0} (MB)'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024))