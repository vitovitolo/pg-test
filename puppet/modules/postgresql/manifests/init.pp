class postgresql
(
	$action = "installed",
	$service = "running",
)
{
	include apt

	package {"postgresql-9.4":
		ensure => "$action",
		require => Exec["apt-get-update"]
	}
	service {"postgresql":
		ensure => "$service",
		require => Package["postgresql-9.4"],
	}
}
