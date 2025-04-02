echo "Making and installing to $1"
make all
if [ $? -eq 0 ]; then
    cp baseset/*.tar $1/baseset/
    cp newgrf/*.grf $1/newgrf/
fi
