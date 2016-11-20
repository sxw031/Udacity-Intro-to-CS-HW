# [Double Gold Star] Memoization is a way to make code run faster by saving
# previously computed results.  Instead of needing to recompute the value of an
# expression, a memoized computation first looks for the value in a cache of
# pre-computed values.

# Define a procedure, cached_execution(cache, proc, proc_input), that takes in
# three inputs: a cache, which is a Dictionary that maps inputs to proc to
# their previously computed values, a procedure, proc, which can be called by
# just writing proc(proc_input), and proc_input which is the input to proc.
# Your procedure should return the value of the proc with input proc_input,
# but should only evaluate it if it has not been previously called.

# run time testing
import time

def time_execution(function,inputs):
	start = time.clock()
	result = function(inputs)
	run_time = time.clock() - start
	return result, run_time

# start cached fibonacci
def cached_execution(cache, proc, proc_input):
    # format of cache: {proc_input1:proc_output1, proc_input2:proc_output2,...}
    if proc_input not in cache:
        cache[proc_input] = proc(proc_input)
    return cache[proc_input]

def cached_fibo(n):
    if n == 1 or n == 0:
        return n
    else:
        return (cached_execution(cache, cached_fibo, n - 1 )
               + cached_execution(cache,  cached_fibo, n - 2 ))

cache = {}
print time_execution(cached_execution,(cache, cached_fibo, 40))



### this is uncached fibonacci
def uncached_fibo(n):
	if n == 1 or n == 0:
		return 1
	else:
		return uncached_fibo(n - 1) + uncached_fibo(n - 2)

print time_execution(uncached_fibo,40)


