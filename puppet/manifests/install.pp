node "default" {
	$username="pg_script"
	$passwd="pg_script"

	class { "postgresql": }

	postgresql::create_role {"populate":
		rolename 	=> "${username}",
		rolepass 	=> "${passwd}",
	}
	class {"psycopg2":}

	class {"pg_scripts":
		username	=> "${username}",
		passwd 		=> "${passwd}",
		default_db 	=> "postgres",
		host 		=> "localhost",
	}
}
