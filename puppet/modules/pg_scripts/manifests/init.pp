class pg_scripts
(
	$username = "postgres",
	$passwd = "postgres",
	$default_db = "postgres",
	$host = "localhost",
)
{
	file {"/opt/pg_scripts":
		ensure => "directory",
	}
	file {"/opt/pg_scripts/bin":
		ensure  => "directory",
		owner   => "root",
		group   => "root",
		source  => 'puppet:///modules/pg_scripts/src',
		links   => "follow",
		recurse => true,
		require => File["/opt/pg_scripts"],
	}
	file {"/opt/pg_scripts/conf":
		ensure => "directory",
		require => File["/opt/pg_scripts"],
	}
	file {"/opt/pg_scripts/conf/config.py":
		ensure  => "file",
		owner   => "root",
		group   => "root",
		mode 	=> 0644,
		content => template("pg_scripts/config.py.erb"),
		require => File["/opt/pg_scripts/conf"],
	}
}
