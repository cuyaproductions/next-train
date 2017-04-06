#!/bin/bash

rm $HOME/bin/next-train
rm -fr $HOME/bin/metros

if [ $? -eq 0 ]
then
  echo "Uninstall of next-train was successful"
  exit 0
fi

echo "ERROR: Uninstall of next-train was unsuccessful"
exit 1