# Write a procedure, rotate which takes as its input a string of lower case
# letters, a-z, and spaces, and an integer n, and returns the string constructed
# by shifting each of the letters n steps, and leaving the spaces unchanged.
# Note that 'a' follows 'z'. You can use an additional procedure if you
# choose to as long as rotate returns the correct string.
# Note that n can be positive, negative or zero.

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
        
def rotate(letters, n):
    # Your code here
    letterstring = ''
    letterlist = []
    for letter in letters:
        letterlist.append(shift_n_letters(letter,n))
    for char in letterlist:
        letterstring = letterstring + char
    return letterstring

# solution 2
def rotate(aString,rotations):
    newString = ""
    for letter in aString:
        if letter == " ":
            newLetter = letter
        else:
            newLetter = chr( ( (ord(letter) - ord('a') + rotations) % 26) + ord('a'))
        newString = newString + newLetter
    return newString

# test
print rotate ('sarah', 13)
#>>> 'fnenu'
print rotate('fnenu',13)
#>>> 'sarah'
print rotate('dave',5)
#>>>'ifaj'
print rotate('ifaj',-5)
#>>>'dave'
print rotate(("zw pfli tfuv nfibj tfiivtkcp pfl jyflcu "
                "sv rscv kf ivru kyzj"),-17)
#>>> ???