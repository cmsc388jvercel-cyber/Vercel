# dev setup
Run the following commands:
`npm install -D @tailwindcss/typography`
`pip install -r requirements.txt`
`pip install --upgrade Flask`
`chmod +x tw.sh`

then open up 2 terminal tabs side by side and run the following commands:
`./tw.sh` // watches for changes to styles in templete files and updates the css
`flask run --debug` // watches for changes in template files and updates the dev server