# weaviate-podcast-search
Search through the Weaviate Podcast!

To run, grab a Weaviate backup from the links below and put it in the `backups` folder, then:

```
docker-compose up -d
python3 restore.py
```

<h2> Weaviate Backups </h2>
<ul>
<li> 12/22:  https://storage.googleapis.com/weaviate-podcast/weaviate-pod.zip</li>
</ul>

<h2> Podcast Transcriptions (note this is the first iteration of this, data needs cleaning badly) </h2>
<ul>
<li> Raw Texts: https://storage.googleapis.com/weaviate-podcast/raw-pod-texts.json.zip </li>
<li> Vectorized Raw Texts: https://storage.googleapis.com/weaviate-podcast/vectorized-raw-pod-texts.json.zip </li>
</ul>
