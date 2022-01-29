#!/usr/bin/env sh

# abort on errors
set -e

# build
npm run build

# navigate into the build output directory
cd dist

# cp index.html 404.html

# if you are deploying to a custom domain
echo 'app.lormaster.com' > CNAME

git init
git add -A
git reset HEAD -- deck.html
git commit -m 'deploy'
git branch -m master main

# if you are deploying to https://<USERNAME>.github.io
# git push -f git@github.com:<USERNAME>/<USERNAME>.github.io.git main

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:LoR-Master/lor-master-web-app.git main:gh-pages

cd -