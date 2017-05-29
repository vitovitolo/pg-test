define postgresql::create_role
(
	$rolename = "test",
	$rolepass = "test",
)
{
	include postgresql
	file {"/usr/local/bin/create_pg_role.sh":
		ensure 	=> file,
		owner 	=> "root",
		group 	=> "root",
		mode 	=> 0775,
		content	=> template("postgresql/create_pg_role.sh.erb")
	}
	exec {"create-role-${rolename}":
		path		=> ["/bin","/usr/bin", "/usr/bin", "/usr/sbin"],
		command 	=> "/usr/local/bin/create_pg_role.sh ${rolename} ${rolepass} ",
		user 		=> "postgres",
		unless		=> "psql -t -c \'\\du\' | cut -d \\| -f 1 | grep -qw ${rolename} ",
		require 	=> [Package["postgresql-9.4"],File["/usr/local/bin/create_pg_role.sh"],Service["postgresql"]],
	}
}
