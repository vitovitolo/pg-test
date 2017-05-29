class psycopg2
(
	$action = "installed",
)
{
	include apt

	package {"python-psycopg2":
		ensure => "$action",
		require => Exec["apt-get-update"],
	}
}
