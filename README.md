# weaviate-podcast-search
Search through the Weaviate Podcast!

Check out the blog here - https://weaviate.io/blog/weaviate-podcast-search!

To run:
```
docker-compose up -d
python3 create-schema.py
python3 upload-clean-pods.py
```

Or just restore the backup! (note may not always be up to date)
```
docker-compose up -d
python3 restore.py
```

Happy searching! I hope you find this useful, thanks so much for watching the Weaviate Podcast!
