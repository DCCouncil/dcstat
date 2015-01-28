cp Final_Q1-Q8_All.pdf pgs/Final_Q1-Q8_All.pdf
cd pgs
pdftk Final_Q1-Q8_All.pdf burst 
cd ..
python lib/burst.py
python lib/compress.py
cd compress
aws s3 sync . s3://dcstat/public --acl public-read --profile council
cd ..
zip dcstat_20.zip compress/*.pdf
python lib/pdf_to_json.py
zip dcstat_20_json.zip json/*.json
aws s3 cp data/metadata.json s3://dcstat --acl public-read --profile council
aws s3 cp dcstat_20.zip s3://dcstat/public/dcstat_20.zip --acl public-read --profile council
aws s3 cp dcstat_20_json.zip s3://dcstat/public/dcstat_20_json.zip --acl public-read --profile council
aws s3 cp dcstat_20.pdf s3://dcstat/public --acl public-read --profile council
rm compress/*.pdf
rm tmp/*.pdf
rm pgs/*.pdf
rm pgs/*.txt
mongo sal
db.dropDatabase()
python lib/json_to_mongo.py
python lib/mongo_fts.py
git commit -am 'updated the files'
git push origin master