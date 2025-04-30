def code():
    print(""" 
          
EXP-1
a)	ODD (or) EVEN:
a=int(input("Enter the Number:"))
if (a%2==0):
    print(a,"is EVEN")
else:
    print(a,"is ODD")
-----------------------
n=int(input("Enter a Number:"))
for i in range(2,n//2):
    if (n%i==0):
        print(n,"is not a prime number")
        break
else:
    print(n,"is a prime number")
------------------------------------
a=int(input("Enter a Number:"))
if (a>0):
    for i in range(a):
        n=(a*(a+1))/2
print(n,"is sum of",a,"natural numbers")
------------------------------------------
a=int(input("Enter the number_1"))
b=int(input("Enter the number_2"))
c=int(input("Enter the number_3"))
if (a > b and a >c):
    print(a, "is the Greatest")
elif (b> a and b >c):
    print(b, "is the Greatest")
elif (c>a and c>b):
    print(c, "is the Greatest")
else:
    print(a,"=",b,"=",c)
------------------------------
a=int(input("Enter a Number:"))
fact=1
if (a>0):
    for i in range(a,0,-1):
        fact=fact*i
print("Factorial of",a,"is",fact)
------------------------------
text = input("Enter a string: ")
vowel_count = 0
for char in text:
    if char in ['a', 'e', 'i', 'o', 'u','A','E','I','O','U']:
        print(char,"is a vowel.")
        vowel_count +=    1
print(f"Total number of vowels: ",vowel_count)
-----------------------------------
a=int(input("Enter a Year:"))
if (a%4==0):
    print(a,"is Leap Year")
else:
    print(a,"is Non-Leap Year")
-------------------------------
day = int(input("Enter a number (1-7) to identify the day of the week: "))
if day== 1:
    print("The day is Monday.")
elif day == 2:
    print("The day is Tuesday.")
elif day == 3:
    print("The day is Wednesday.")
elif day == 4:
    print("The day is Thursday.")
elif day == 5:
    print("The day is Friday.")
elif day == 6:
    print("The day is Saturday.")
elif day == 7:
    print("The day is Sunday.")
else:
    print("Invalid input! Please enter a number between 1 and 7.")
-------------------------------------------

EXP-2
EASY:
	a=25
if (a%2==0):
    print(a,"is Even")
else:
    print(a,"is ODD")

 
MEDIUM:
 a=int(input("Enter a Number: "))
if (a%2==0):
    print(a,"is Even")
else:
    print(a,"is ODD")
 
HARD:
def evenOdd(x):
    if (x % 2 == 0):
        print(x,"is even")
    else:
        print(x,"is odd")
evenOdd(int(input("Enter a Number: ")))
Sample Output

 
a)	PRIME NUMBER       :
num = 11
for i in range(2, num//2):
    if (num % i) == 0:
        print(num, "is not a prime number")
        break
else:
    print(num, "is a prime number")
Sample Output
 


MEDIUM:
num = int(input("Enter a Number: "))
if num > 1:
    for i in range(2, (num//2)+1):
        if (num % i) == 0:
            print(num, "is not a prime number")
           break
 else:
        print(num, "is a prime number")
else:
    print(num, "is not a prime number")
Sample Output
 

HARD:
def is_prime(n):
    i=2
    while range(2, (n//2)+1):
        if n % i == 0:
            print(n, "is not a prime number")
            break
        else:
            print(n, "is a prime number")
            break
is_prime(int(input("Enter a Number: ")))

Sample Output

 
a)	NATURAL NUMBERS:
EASY:
	a=5
if (a>0):
        n=(a*(a+1))/2
print(n,"is sum of",a,"natural numbers")
Sample Output
 
MEDIUM:
def sum(N):
   		 total = 0
  	 	 count = 1
  	 	 while count <= N:
      	 		 total += count
        			count += 1
   		 return total
N = 7
result = sum(N)
print("The Sum of the First", N, "Natural Numbers is:",result)
Sample Output
 

HARD:
def get_positive_integer():
	while True:
    	try:
        	n = int(input("Enter a positive integer: "))
        	if n <= 0:
            	raise ValueError("The number must be positive.")
        	return n
    	except ValueError as e:
        	print(f"Invalid input: {e}")

def recursive_sum(n):
	if n == 1:
    	return 1
	else:
    	return n + recursive_sum(n - 1)

def main():
	print("This program calculates the sum of the first n natural numbers using recursion.")
	n = get_positive_integer()
	result = recursive_sum(n)
	print(f"The sum of the first {n} natural numbers is: {result}")

if _name_ == "_main_":
	main()

Sample Output
 
a)	Greatest among three:
EASY:
a=4
b=7
c=8
if (a > b and a >c):
    print(a, "is the Greatest")
elif (b> a and b >c):
    print(b, "is the Greatest")
elif (c>a and c>b):
    print(c, "is the Greatest")
else:
    print(a,"=",b,"=",c)
Sample Output
 
MEDIUM:
a=int(input("Enter the number_1: "))
b=int(input("Enter the number_2: "))
c=int(input("Enter the number_3: "))
if (a > b and a >c):
    print(a, "is the Greatest")
elif (b> a and b >c):
    print(b, "is the Greatest")
elif (c>a and c>b):
    print(c, "is the Greatest")
else:
    print(a,"=",b,"=",c)
Sample Output
 
HARD:
def maximum(a, b, c): 

    if (a >= b) and (a >= c): 
        largest = a 

    elif (b >= a) and (b >= c): 
        largest = b 
    else: 
        largest = c 
        
    print(largest,"is the largest") 

a=int(input("Enter the number_1: "))
b=int(input("Enter the number_2: "))
c=int(input("Enter the number_3: "))
print(maximum(a, b, c)) 
Sample Output

 

a)	FACTORIAL:
EASY:
a=5
fact=1
if (a>0):
    for i in range(a,0,-1):
        fact=fact*i
print("Factorial of",a,"is",fact)
Sample Output
 
MEDIUM:
 a=int(input("Enter a Number:"))
fact=1
if (a>0):
    for i in range(a,0,-1):
        fact=fact*i
print("Factorial of",a,"is",fact)

Sample Output

 

HARD:
def factorial(n):

    return 1 if (n==1 or n==0) else n * factorial(n - 1) 

num =int(input("Enter a Number:"))
print("Factorial of",num,"is",factorial(num))
Sample Output

 
a)	COUNTING VOWELS:
EASY:
atext = input("Enter a string: ")
vowel_count = 0
for char in text:
 if char in ['a', 'e', 'i', 'o', 'u','A','E','I','O','U']:
 print(char,"is a vowel.")
  vowel_count += 1
print(f"Total number of vowels: ",vowel_count)
Sample Output
 
MEDIUM:
def count_vowels(s):
    vowels = "aeiouAEIOU"
    vowel_list = [char for char in s if char in vowels]
    count = len(vowel_list)
    return {"count": count, "vowels": vowel_list}
text = input("Enter a string: ")
result = count_vowels(text)
print(f"Vowel Count: {result['count']}, Vowels: {result['vowels']}")
Sample Output
 


HARD:
import re
def vow(s):
    vowels = re.findall(r'[aeiouAEIOU]', s)  # Extracts all vowels using regex
    count = len(vowels)
    
    return {"count": count, "vowels": vowels}

text = input("Enter a string: ")
result = vow(text)
print(f"Vowel Count: {result['count']}, Vowels: {result['vowels']}")
Sample Output

 
a)	LEAP YEAR:
EASY:
a=2025
if (a%4==0):
  print(a,"is Leap Year")
else:
print(a,"is Non-Leap Year")
Sample Output
 
MEDIUM:
 a=int(input("Enter a Year:"))
if (a%4==0):
    print(a,"is Leap Year")
else:
    print(a,"is Non-Leap Year")
ample Output
 




HARD:
a=int(input("Enter a Year:"))

def year(a):
    if (a%4==0):
        print(a,"is Leap Year")
    else:
        print(a,"is Non-Leap Year")
y=year(a)
Sample Output
 

a)	DAY OF THE WEEK:
EASY:
	day = int(input("Enter a number (1-7) to identify the day of the week: "))

if day== 1:
    print("The day is Monday.")
elif day == 2:
    print("The day is Tuesday.")
elif day == 3:
    print("The day is Wednesday.")
elif day == 4:
    print("The day is Thursday.")
elif day == 5:
    print("The day is Friday.")
elif day == 6:
    print("The day is Saturday.")
elif day == 7:
    print("The day is Sunday.")
else:
    print("Invalid input! Please enter a number between 1 and 7.")
Sample Output
 

MEDIUM:
import calendar
def findDay(date):
    day, month, year = (int(i) for i in date.split(' ')) 
    dayNumber = calendar.weekday(year, month, day)
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return days[dayNumber]
# Driver program
date = input("Enter date (e.g., '10 02 2025'): ")
print(findDay(date))
Sample Output
 




HARD:
from dateutil import parser

def get_day_pro(date_str):
    date_obj = parser.parse(date_str)  # Automatically parses different date formats
    return date_obj.strftime("%A")  # Returns full weekday name

# Example Usage
date_input = input("Enter date (e.g., '10-02-2025' or 'February 10, 2025'): ")
print(f"Day of the Week: {get_day_pro(date_input)}")
          
          
EXP-3
def swap(s1,s2):
    if len(s1)>0 and len(s2)>0:
        ns1=s1[0]+s2[1:]
        ns2=s2[0]+s1[1:]
        result=ns1 +" "+ ns2
        return result
    else:
        return "Both strings should have atleast one character"
s1=input("Enter String_1: ")
s2=input("Enter String_2: ")
print(swap(s1,s2))
------------------------------
def replace(s):
    f1=s[0]
    rep=f1+s[1:].replace(f1,"#")
    return rep 
s=input("Enter String_: ")
print(replace(s))
--------------------------
def freq(text):
    fw=text.split()
    fw_count={}

    for word in fw:
        if word in fw_count:
            fw_count[word]+=1
        else:
            fw_count[word]=1
    s_count=sorted(fw_count.items(),key=lambda x: x[1],reverse=True)
    if len(s_count)>1 :
        global count
        count=s_count[1]
        return count
    else:
        return "Not enough unique words."
text="I realized my happiness was artificial. I felt happy my because I saw the others were happy and because I knew I should feel happy, but I wasn't really happy."
print(freq(text))
---------------------------------
def count_substring_occurrences(main_string, sub_string):
    count = main_string.count(sub_string)
    return count
# Taking input from the user
main_string = input("Enter the main string: ")
sub_string = input("Enter the substring to count: ")
# Counting occurrences
result = count_substring_occurrences(main_string, sub_string)
print("Input:", main_string)
print("Sub-String:", sub_string)
print("Occurence:", result)
-----------------------------------
def sort_words_alphabetically():
    words = input("Enter a comma-separated sequence of words: ").split(', ')
    sorted_words = sorted(words)
    print("Output:", ', '.join(sorted_words))
# Calling the function
sort_words_alphabetically()
--------------------------------
def replace_not_bad(sentence):
    not_index = sentence.find('not')
    bad_index = sentence.find('bad')
    
    if not_index != -1 and bad_index != -1 and not_index < bad_index:
        return sentence[:not_index] + 'good' + sentence[bad_index + 3:]
    return sentence
# Taking input from the user
sentence = input("Enter a sentence: ")
# Replacing 'not'...'bad' with 'good'
result = replace_not_bad(sentence)
print("Output:", result)
-----------------------------------       

EXP-4
def find_second_largest_smallest(lst):
    unique_sorted_list = sorted(set(lst))  # Remove duplicates and sort
    print("The second largest element is:", unique_sorted_list[-2])
    print("The second smallest element is:", unique_sorted_list[1])

# Example usage
numbers = [12, 45, 2, 41, 31, 10, 8, 6, 4]
find_second_largest_smallest(numbers)
---------------------------------------
def frequency_count(lst):
    freq = {}  # Dictionary to store frequency
    for num in lst:
        freq[num] = freq.get(num, 0) + 1
    print("Element | Frequency")
    for key, value in freq.items():
        print(f"{key} | {value}")
# Example usage
numbers = [1, 2, 8, 3, 2, 2, 2, 5, 1]
frequency_count(numbers)
--------------------------------------
def remove_duplicates(lst):
    unique_elements = set(lst)  # Convert list to set to remove duplicates
    print(unique_elements)
# Example usage
a = [10, 20, 30, 20, 10, 50, 60, 40, 80, 50, 40]
remove_duplicates(a)
------------------------------------------
numbers = (1, 2, 3, 4, 2, 5, 2, 6)
# Count occurrences of 2
count_2 = numbers.count(2)
print("The number 2 appears", count_2, "times.")
------------------------------------------
# Define a tuple
fruits = ("apple", "banana", "cherry", "banana", "orange")
# Find index of 'banana'
index_banana = fruits.index("banana")
print("The first occurrence of 'banana' is at index:", index_banana)
----------------------------------------
# Define two tuples
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
# Concatenate tuples
merged_tuple = tuple1 + tuple2
print("Merged Tuple:", merged_tuple)
---------------------------------------

EXP-5
key=int(input('Enter a Key:'))
a={1:'abc',2:'acb',3:123}
if key in a.keys():
    print('Given key already exists')
else:
    print('Given Key does not exists')
-------------------------------------
def ltod(list):
    if not list:
        return {}
    return {list[0]:ltod(list[1:])}
user_input = list(map(int, input("Enter numbers separated by space: ").split()))
nested_dic=ltod(user_input)
print(nested_dic)
----------------------------------------
# initializing dictionary
test_dict = {'gfg': 10, 'is': 15, 'best': 20, 'for': 10, 'geeks': 20}
# printing original dictionary
print("The original dictionary is : " + str(test_dict))
# Remove duplicate values in dictionary
# Using dictionary comprehension
temp = {val: key for key, val in test_dict.items()}
res = {val: key for key, val in temp.items()}
# printing result
print("The dictionary after values removal : " + str(res))
-------------------------------------------
          
 EXP-6
def copy_file(src, dest):
    with open(src, 'r') as s, open(dest, 'w') as d:
        d.write(s.read())

# Example usage
copy_file('source.txt', 'destination.txt')
-------------------------------------
def read_n_lines(filename, n):
    with open(filename, 'r') as file:
        for _ in range(n):
            print(file.readline(), end='')
# Example usage
read_n_lines('source.txt', 3)  # Reads the first 3 lines
---------------------------------------------
def extract_vowel_words(filename):
    vowels = ('A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u')
    with open(filename, 'r') as file:
        words = file.read().split()  # Read and split text into words
        vowel_words = [word for word in words if word.startswith(vowels)]
        print("Words starting with a vowel:", vowel_words)
# Example usage
extract_vowel_words('example.txt')
--------------------------------------
def find_longest_word(filename):
    with open(filename, 'r') as file:
        words = file.read().split()  # Read and split text into words
    longest_word = max(words, key=len)  # Find the longest word
    print("Longest word:", longest_word)
# Example usage
find_longest_word('example.txt')
-------------------------------------------         
""")