from django.test import TestCase
import random
import string

strr = ''.join(random.choices(string.digits,k=8))
print(strr)
