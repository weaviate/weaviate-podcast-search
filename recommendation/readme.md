# Ref2Vec Podcast Clip Recommendation Demo

Welcome to the Podcast Clip Recommendation Demo using Weaviate's `ref2vec`!

To run, first init Weaviate with:

```bash
cd weaviate-init
docker-compose up -d
python3 restore.py
```

This will restore a backup that has LLM-generated pod clip summaries.

Once you've initialized Weaviate, you can now run the front-end from the main folder

```bash
cd ..
uvicorn main:app --reload
```

Note the `cd ..` is just to navigate out of the weaviate-init folder and back into the main folder.