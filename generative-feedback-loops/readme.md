# Generative Feedback Loops

This folder demonstrates a Generative Feedback Loop with the Weaviate Podcast Transcripts to write a summary of each podcast clip and save that summary **back** to each PodClip data object!

This folder is intended to be standalone meaning everything you need to run it is contained in this folder.

```bash
docker-compose up -d
python3 create-schema.py
python3 upload-clean-pods.py
python3 backup.py
```

The current intention is that you can restore these backups in either the main `search` app or the `recommendation` demo.

Please let us know if you have any questions!