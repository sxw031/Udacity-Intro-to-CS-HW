# Question 1. shift a letter
# Write a procedure, shift, which takes as its input a lowercase letter,
# a-z and returns the next letter in the alphabet after it, with 'a' 
# following 'z'.

# solution 1
def shift(letter):
    string = "abcdefghijklmnopqrstuvwxyz"
    pos = string.find(letter)
    if pos == 25:
        return 'a'
    else:
        return string[pos+1]

# solution 2
# the ord() convert a single character string into an ASCII number.
# the chr() convert the ASCII number back to a single character string.
def shift(letter):
    if letter == 'z':
        return 'a'
    else:
        return chr(ord(letter)+1)

# solution 3
# inspired by @Simon-454678 of Udacity forum
# shift 1 letter: generalized formula: ( y = (x - x0 + 1) % 26 ) + x0
# where
#  y = position of shifted clock with respect to original clock
#  x0 = position at original clock
#  k = number of elements in the clock. 

def shift(letter):   
    return chr((ord(letter) - ord('a') + 1)%26 + ord('a'))

# test 
print shift('a')
#>>> b
print shift('n')
#>>> o
print shift('z')
#>>> a


# Question 2 - shift n letters
# Write a procedure, shift_n_letters which takes as its input a lowercase
# letter, a-z, and an integer n, and returns the letter n steps in the
# alphabet after it. Note that 'a' follows 'z', and that n can be positive,
# negative or zero.

# solution 1
def shift_n_letters(letter, n):
    strings = 'abcdefghijklmnopqrstuvwxyz'
    pos = strings.find(letter)
    if n == 26:
        return letter
    if pos+n <= 25:
        return strings[pos+n]
    else:
        return strings[(pos+n-1) % 25]

# solution 2
def shift_n_letters(letter, n):
    return chr((ord(letter) - ord('a') + n)%26 + ord('a'))


print shift_n_letters('s', 1)
#>>> t
print shift_n_letters('s', 2)
#>>> u
print shift_n_letters('s', 10)
#>>> c
print shift_n_letters('s', -10)
#>>> i