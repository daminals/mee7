#!/bin/bash
cd "$(dirname "$0")"


output=$(git remote)
while read -r; do
		if [[ "$output" == *"origin"* ]]; then
				 git push origin master
				 if [[ "$output" == *"heroku"* ]]; then
						 git push heroku master
				 fi
		elif [[ "$output" == *"heroku"* ]]; then
				 git push heroku master
		else
				echo "no remotes"
				echo $output
fi
done <<< $output

