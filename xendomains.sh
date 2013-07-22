#!/bin/bash

if ! [ -e /proc/xen/privcmd ]; then
	exit 0
fi

TOOLSTACK=$(/usr/lib/xen/bin/xen-toolstack toolstack 2>/dev/null)
if [ $? -ne 0 ]; then
	echo "No usable Xen toolstack selected"
	exit 0
fi
if [ "$(basename "$TOOLSTACK")" != xl ] && [ "$(basename "$TOOLSTACK")" != xm ]; then
	exit 0
fi

if ! /usr/lib/xen/bin/xen-toolstack list >/dev/null 2>&1 ; then
	exit 0;
fi

[ -r /etc/sysconfig/xendomains ] && . /etc/sysconfig/xendomains

shopt -s nullglob

check_config_name()
{
	/usr/lib/xen/bin/xen-toolstack create --quiet --dryrun --defconfig "$1" | sed -n 's/^.*\("name":"\([^"]*\)",.*\)\|(name \(.*\))$/\2\3/p'
}

check_running()
{
	/usr/lib/xen/bin/xen-toolstack domid "$1" >/dev/null 2>&1
	return $?
}

timeout_coproc()
{
	local TIMEOUT=$1
	shift

	coproc "$@" >/dev/null 2>&1

	local COPROC_OUT
	exec {COPROC_OUT}<&"${COPROC[0]}"
	local PID="$COPROC_PID"

	for no in $(seq 0 $TIMEOUT); do
		if [ -z "$COPROC_PID" ]; then break; fi
		sleep 1
	done

	kill -INT "$COPROC_PID" >/dev/null 2>&1
	wait $PID
	local rc=$?
	if [ $rc -eq 0 ]; then
		echo "ok"
	else
		echo "fail ($rc)"
	fi

	[ $rc -gt 0 ] && cat <&$COPROC_OUT
	exec <&$COPROC_OUT-
}

timeout_domain()
{
	name="$1"
	TIMEOUT="$2"
	for no in $(seq 0 $TIMEOUT); do
		if ! check_running "$name"; then return 0; fi
		sleep 1
	done
	return 1
}

do_start_restore()
{
	[ -n "$XENDOMAINS_SAVE" ] || return
	[ -d "$XENDOMAINS_SAVE" ] || return
	[ -n "$XENDOMAINS_RESTORE" ] || return

	for file in $XENDOMAINS_SAVE/*; do
		if [ -f $file ] ; then
			name="${file##*/}"
			echo -n "Restoring Xen domain $name (from $file): "

			out=$(/usr/lib/xen/bin/xen-toolstack restore "$file" >/dev/null 2>&1)
			case "$?" in
				0)
					rm "$file"
					domains[$name]='started'
					echo "ok"
					;;
				*)
					domains[$name]='failed'
					echo "fail"
					echo "$out"
					;;
			esac
		fi
	done
}

do_start_auto()
{
	[ -n "$XENDOMAINS_AUTO" ] || return
	[ -d "$XENDOMAINS_AUTO" ] || return

	for file in $XENDOMAINS_AUTO/*; do
		name="$(check_config_name $file)"

		if [ "${domains[$name]}" = started ]; then
			:
		elif check_running "$name"; then
			echo "Xen domain $name already running"
		else
			echo -n "Starting Xen domain $name (from $file): "

			if [ "${domains[$name]}" = failed ]; then
				echo "fail"
			else
				out=$(/usr/lib/xen/bin/xen-toolstack create --quiet --defconfig "$file" >/dev/null 2>&1)
				case "$?" in
					0)
						echo "ok"
						;;
					*)
						echo "fail"
						echo "$out"
						;;
				esac
			fi
		fi
	done
}

do_start() 
{
	declare -A domains

	do_start_restore
	do_start_auto
}

do_stop_migrate()
{
	[ -n "$XENDOMAINS_MIGRATE" ] || return

	while read id name rest; do
		echo -n "Migrating Xen domain $name ($id): "
		(timeout_coproc "$XENDOMAINS_STOP_MAXWAIT" /usr/lib/xen/bin/xen-toolstack migrate $id $XENDOMAINS_MIGRATE)
	done < <(/usr/lib/xen/bin/xen-init-list)
}

do_stop_save()
{
	[ -n "$XENDOMAINS_SAVE" ] || return
	[ -d "$XENDOMAINS_SAVE" ] || mkdir -m 0700 -p "$XENDOMAINS_SAVE"

	while read id name rest; do
		echo -n "Saving Xen domain $name ($id): "
		(timeout_coproc "$XENDOMAINS_STOP_MAXWAIT" /usr/lib/xen/bin/xen-toolstack save $id $XENDOMAINS_SAVE/$name)
	done < <(/usr/lib/xen/bin/xen-init-list)
}

do_stop_shutdown()
{
	while read id name rest; do
		echo -n "Shutting down Xen domain $name ($id): "
		/usr/lib/xen/bin/xen-toolstack shutdown $id >/dev/null 2>&1
		rc=$?
		if [ $rc -eq 0 ]; then
			echo "ok"
		else
			echo "fail ($rc)"
		fi
	done < <(/usr/lib/xen/bin/xen-init-list)
	while read id name rest; do
		echo -n "Waiting for Xen domain $name ($id) to shut down: "
		timeout_domain "$name" "$XENDOMAINS_STOP_MAXWAIT"
		rc=$?
		if [ $rc -eq 0 ]; then
			echo "ok"
		else
			echo "fail ($rc)"
		fi
	done < <(/usr/lib/xen/bin/xen-init-list)
}

do_stop()
{
	do_stop_migrate
	do_stop_save
	do_stop_shutdown
}

case "$1" in
	start)
		do_start
		;;
	stop)
		do_stop
		;;
	restart)
		do_stop
		do_start
		;;
	reload|force-reload)
		do_stop
		do_start
		;;
	status)
		/usr/lib/xen/bin/xen-toolstack list -v
		;;
	*)
		echo "Usage: $0 {start|stop|status|restart|reload|force-reload}"
		exit 3
		;;
esac

exit 0
