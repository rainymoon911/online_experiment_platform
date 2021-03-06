import ldap

ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
l = ldap.initialize("ldap://192.168.1.116:389")
//l = ldap.initialize("ldaps://192.168.1.116:636")
l.set_option(ldap.OPT_REFERRALS, 0)
l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
l.set_option( ldap.OPT_X_TLS_DEMAND, True )
l.set_option( ldap.OPT_DEBUG_LEVEL, 255 )
baseDN = "ou=Users,dc=openedx,dc=com"
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = None
searchFilter = "cn=*z*"
ldap_result_id = l.search(baseDN, searchScope, searchFilter)
result_set = []
while 1:
    result_type, result_data = l.result(ldap_result_id, 0)
    if (result_data == []):
        break
    else:
        if result_type == ldap.RES_SEARCH_ENTRY:
            result_set.append(result_data)
    print result_set
