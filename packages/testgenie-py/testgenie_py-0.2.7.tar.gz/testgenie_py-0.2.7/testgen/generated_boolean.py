def bin_and(a: bool, b: bool):
    if a == True:
        if b == True:
            return True
        else:
            return False
    else:
        if b == True:
            return False
        else:
            return False

def bin_xor(a: bool, b: bool):
    if a == True:
        if b == True:
            return False
        else:
            return True
    else:
        if b == True:
            return True
        else:
            return False

def status_flags(active: bool, verified: bool, admin: bool):
    if active == True:
        if verified == True:
            if admin == True:
                return 'admin-verified'
            else:
                return 'user-verified'
        else:
            if admin == True:
                return 'admin-unverified'
            else:
                return 'user-unverified'
    else:
        if verified == True:
            if admin == True:
                return 'admin-verified'
            else:
                return 'inactive'
        else:
            if admin == True:
                return 'admin-unverified'
            else:
                return 'inactive'

