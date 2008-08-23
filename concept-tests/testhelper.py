import ldap, ldif, ldaphelper

l = ldap.initialize('ldap://localhost')
l.bind_s('cn=admin,dc=fluidsignal,dc=com', 'Aiphootah3')

raw = l.search_s('dc=fluidsignal,dc=com', ldap.SCOPE_SUBTREE)
res = ldaphelper.get_search_results(raw)

for i in res:
    print i.to_ldif()


