class pg_scripts::uninstall
(
)
{
	file {"/opt/pg_scripts":
		ensure => "absent",
		force  => true,
	}
}
