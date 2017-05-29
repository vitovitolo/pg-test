node "default" {

	class { "postgresql":
		action => "absent",
		service => "stopped",
	}
	package{["postgresql-client-9.4","postgresql-common","postgresql-client-common"]:
		ensure => "purged",
	}
	file {"/usr/local/bin/create_pg_role.sh":
		ensure => "absent",
	}
	class {"psycopg2":
		action => "absent",
	}
	class {"pg_scripts::uninstall":}
}
