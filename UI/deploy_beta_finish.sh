#!/usr/bin/env sh

# abort on errors
set -e

# navigate into the build output directory
cd beta_finish

# cp index.html 404.html

echo "User-agent: *
Disallow: /
" > robots.txt
echo "beta.lormaster.com" > CNAME

# if you are deploying to a custom domain

git init
git add -A
git commit -m 'deploy'
git branch -m master main

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:LoR-Master/lor-master-web-app-beta.git main:gh-pages

cd -