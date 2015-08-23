class Config:

    CONFIG = {
        "GIT":
        {
            # GitLab's host and port, make sure open-edx can access
            "HOST" : "192.168.1.62",
            "PORT" : 80,

            # GitLab admin account's token
            "ADMIN_TOKEN": "Gysy4D6M1-B6sTNtyu2S",

            # Teacher account information, be used to create repo/project
            "TEACHER":
            {
                "TOKEN": "yTzMzxy76bA3wizyUTHM"
            }
        },

        "DOCKER":
        {
            # Default docker image's namespace, for example, "mynamespace/mydocker1"
            "NAMESPACE": "uclassroom",

            # memory for each container
            "MEM_LIMIT": "256m",

            # Container's host, may be same as docker server's host,
            # could be visited by students' browsers
            "HOST"   : "mooc.enight.me",

            # URL and TLS information of remote docker server
            "REMOTE_API":
            {
                "URL"    : "2376",  # url of docker host
                "PORT"   : 2376,                       # port of docker daemon
                "CA"     : "/home/zyu/.docker/ca.pem",  # ca file at local
                "CERT"   : "/home/zyu/.docker/cert.pem",  # cert file at local
                "KEY"    : "/home/zyu/.docker/key.pem",  # key file at local
                "VERSION": "1.17"  # docker remote api version
            }
        },
	"LDAP":
	{
	    "PRINCIPAL_NAME":"cn=admin,dc=openedx,dc=com",
	    "PASSWORD"      :"p@ssw0rd",
	    "LDAP_URL"      :"ldap://192.168.1.116:389",
	    "BASE_DN"       :"ou=Users,dc=openedx,dc=com"
	}
    }
