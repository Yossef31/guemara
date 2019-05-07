import re

def validate_password(password):
	if len(password) < 8:
		return False
	elif re.search('[0-9]',password) is None:
		return False
	elif re.search('[A-Z]',password) is None:
		return False
	elif re.search('[a-z]',password) is None:
		return False
	else:
		return True 

# re = regex , permet de rechercher dans une string

# >>> from utils import validate_password
# >>> a='qwert'
# >>> validate_password(a)
# False
# >>> a='Aq12wert'
# >>> validate_password(a)
# True
# >>> a='aq12wert'
# >>> validate_password(a)
# False
# >>> 


