#!/bin/bash


dir="$HOME/bin"

cp ./next-train.py $dir
mv $dir/next-train.py $dir/next-train
chmod +x $dir/next-train

if [ $? -eq 0 ]
then
  echo "next-train installed successfully"
  exit 0
fi

echo "ERROR: next-train did not install successfully"
exit 1