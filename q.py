queries = {
	'users': {
		'table': 'esas.users',
		'pk': ['userType','surname','name'],
		'unic': ['login', 'hashedPass'],
		'fields': ['email', 'phone', 'birthday', 'address', 
					'photo', 'permissionLvl'],
		'ints': ['permissionLvl'],
	},
	'students': {
		'table': 'esas.students',
		'pk': ['studyYear','studyGroup','sSurname','sName'],
		'fields': ['sAddress', 'sEmail', 'sPhone', 'sBirthday', 'sPhoto', 'isFullFamily', 
					'p1FullName', 'p1Phone', 'p2FullName','p2Phone','financialCase','medicalConditions'],
		'unic': ['sId'],
		'ints': ['studyYear'],
	},
	'grades': {
		'table': 'esas.grades',
		'pk': ['studyYear','studyGroup','subject' ,'sSurname','sName'],
		'fields': ['midGrade', 'finalGrade', 'p1FullName', 'p1Phone', 'p2FullName', 'p2Phone'],
		'unic': ['sId'],
		'ints': ['midGrade','finalGrade','overallGrade','studyYear'],
	},
}


def select(d,q):
	arr = []
	for i in q.get('pk'):

		temp = d.get(i).get()

		if temp != '':
			if i in q.get('ints'):
				arr.append("{} = {}".format(i,temp))
			else:
				arr.append("{} = '{}'".format(i,temp))

	for i in q.get('unic'):

		temp = d.get(i).get()

		if temp != '':
			if i in q.get('ints'):
				arr.append("{} = {}".format(i,temp))
			else:
				arr.append("{} = '{}'".format(i,temp))


	for i in q.get('fields'):

		temp = d.get(i).get()

		if temp != '':
			if i in q.get('ints'):
				arr.append("{} = {}".format(i,temp))
			else:
				arr.append("{} = '{}'".format(i,temp))


	result = '''SELECT * 
FROM {} 
WHERE {} allow filtering;'''.format(q.get('table'), ' AND '.join(arr))

	return result

def insert(d,q):
	arr = []
	arr2 = []
	for i in q.get('pk'):

		temp = d.get(i).get()

		if temp == '':
			return 'You should fill all * fields'
		arr2.append(i)

		if i in q.get('ints'):
			arr.append(temp)
		else:
			arr.append("'{}'".format(temp))

	for i in q.get('unic'):

		temp = d.get(i).get()

		if temp == '':
			return 'You should fill all * fields'
		arr2.append(i)
		if i in q.get('ints'):
			arr.append(temp)
		else:
			arr.append("'{}'".format(temp))


	for i in q.get('fields'):

		temp = d.get(i).get()

		if temp != '':
			arr2.append(i)
			if i in q.get('ints'):
				arr.append(temp)
			else:
				arr.append("'{}'".format(temp))
	result = '''INSERT INTO {} 
({}) values
({}) '''.format(q.get('table'),','.join(arr2), ','.join(arr))

	result+=';'

	return result

def delete(d,q):
	arr = []
	for i in q.get('pk'):

		temp = d.get(i).get()

		if temp == '':
			return 'You should fill all fields'

		if i in q.get('ints'):
			arr.append("{} = {}".format(i,temp))
		else:
			arr.append("{} = '{}'".format(i,temp))


	result = '''DELETE FROM {} 
WHERE {}'''.format(q.get('table'), ' AND '.join(arr))

	return result

def update(d,q):
	arr = []
	for i in q.get('pk'):

		temp = d.get(i).get()

		if temp == '':
			return 'You should fill all fields'


		if i in q.get('ints'):
			arr.append("{} = {}".format(i,temp))
		else:
			arr.append("{} = '{}'".format(i,temp))

	new = []

	for i in q.get('fields'):

		temp = d.get(i).get()

		if temp != '':
			if i in q.get('ints'):
				arr.append("{} = {}".format(i,temp))
			else:
				arr.append("{} = '{}'".format(i,temp))

	result = '''UPDATE {} 
set {}
WHERE {}'''.format(q.get('table'),' , '.join(new),' AND '.join(arr))
	
	result+=';'

	return result



