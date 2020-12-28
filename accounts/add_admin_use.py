from. import admin
import os
BASE = os.path.dirname(os.path.abspath(__file__))

emp_name_handle = open(os.path.join(BASE, 'users.txt'))
def action_grabber():
    with open(os.path.join(BASE, 'users.txt')) as f:
        mylist = [line.strip('\n') for line in f]
        return mylist



def admin_body(username,count):
    fd = open(os.path.join(BASE, 'admin.py'), 'r')
    d = fd.read()
    fd.close()
    m = d.split("\n")
    s = "\n".join(m[0:-2])
    fd = open(os.path.join(BASE, 'admin.py'), 'w+')
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()

    admin_handle=open(os.path.join(BASE, 'admin.py'),'a+')
    admin_handle.write(f"\n    def transfer_to_{username}(self, request, queryset):\n")
    admin_handle.write(f"        all=queryset.values().all().update(assigned=User.objects.get(id={count}))\n")
    admin_handle.write(f"    transfer_to_{username}.short_description = 'Transfer to {username}'\n")
    admin_handle.write('admin.site.register(Final,OrderAdmin)\n')
    admin_handle.close()

def user_adder(username):
    user=open(os.path.join(BASE, 'users.txt'),'a+')
    user.write(f'transfer_to_{username}\n')
    user.close()
   #count is remaining to be added


def user_delete(username,count):
    a_file = open(os.path.join(BASE, 'admin.py'),'r')
    lines = a_file.readlines()
    a_file.close()

    new_file = open(os.path.join(BASE, 'admin.py'),'w')
    for line in lines:
        if line.strip("\n") == f"    def transfer_to_{username}(self, request, queryset):":
            pass
        elif line.strip("\n") == f"        all=queryset.values().all().update(assigned=User.objects.get(id={count}))":
            pass
        elif line.strip("\n") == f"    transfer_to_{username}.short_description = 'Transfer to {username}'":
            pass
        else:
            new_file.write(line)
    new_file.close()
    with open(os.path.join(BASE, 'users.txt'),'r') as f:
        lines = f.readlines()
    with open(os.path.join(BASE, 'users.txt'),'w') as f:
        for line in lines:
            if line.strip("\n") != f'transfer_to_{username}':
                f.write(line)








