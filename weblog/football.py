#coding=utf8
"Why football? just because I watch football game TV while I was coding."



def month_name(month, short=True):
	monthes = {
		1  : ('January', 'Jan'),
		2 : ('February', 'Feb'),
		3 : ('March', 'Mar'),
		4 : ('April', 'Apr'),
		5 : ('May', 'May'),
		6 : ('June', 'Jun'),
		7 : ('July', 'Jul'),
		8 : ('August', 'Aug'),
		9 : ('September', 'Sep'),
		10 : ('October', 'Oct'),
		11 : ('November', 'Nov'),
		12 : ('December', 'Dec'),
	}
	if short:
		return monthes[month][1]
	else:
		return monthes[month][0]
		