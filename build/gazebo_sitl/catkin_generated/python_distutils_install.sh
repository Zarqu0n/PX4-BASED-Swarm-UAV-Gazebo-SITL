#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/zarquon/Project/SwarmDrone/src/gazebo_sitl"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/zarquon/Project/SwarmDrone/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/zarquon/Project/SwarmDrone/install/lib/python3/dist-packages:/home/zarquon/Project/SwarmDrone/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/zarquon/Project/SwarmDrone/build" \
    "/home/zarquon/miniconda3/envs/Noetic/bin/python3" \
    "/home/zarquon/Project/SwarmDrone/src/gazebo_sitl/setup.py" \
     \
    build --build-base "/home/zarquon/Project/SwarmDrone/build/gazebo_sitl" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/zarquon/Project/SwarmDrone/install" --install-scripts="/home/zarquon/Project/SwarmDrone/install/bin"
