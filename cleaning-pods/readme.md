Cleaning the podcasts with GPT3!

```
Please clean the following raw audio transcription to remove "ums" and "likes", as well as generally read like it was written rather than spoken. Please also be mindful that the audio transcription often mistakes "Weaviate" with "V8" or "V eight", please correct this as well to reference "Weaviate".

Here is an example of this:

Original Transcription: Yeah, that's, that's definitely hard to, to debug this. Um, first I would say there's like a big, big need for this. So me as a German speaker, I mean, it's always nice if I go to English, there are like so many models and systems available. But if you, even if you go to German and German, I mean, it's still like a high resource language, has a decent amount of population.

            it's quite powerful economically, but still the number of things you can get is like really limited and it's like really frustrating to see that in English. You can build these amazing semantic switch systems, which works extremely good for q and a retrieval. But even if you go to German, there's like hardly any models available.
            
            And then if you go further down the the language letter to like more and more low resource languages, it's getting harder and harder to. Second motivation is multi building. Multilingual search with lexile search is like really painful. Um, so, so if you build this in elastic search, for example, you need to know the language.
            
            Uh, so you need to know the language of the document, very language. You have like a different index. Um, cause every language requests a different tokenize. Requires a different stock worth list, requires, uh, different stemer. So at the end, let's say you want to target, I dunno, European Union with, I dunno, 20 languages.
            
            You have like 20 different indices and elastic search. And would each has like a different tokenize stemer stock worth list. . For each document you have to run language identification to see, is it a German document or a French document? Mm-hmm. . And then the big challenge comes at query time. Is it like a German query or a French query or an English query?
            
            For some really short queries, it's like a bik. It can be English and German or French and Spanish. And so how do you query these different INDCs? Cause a Spanish query, you have to add like a Spanish index and. But with dance retrievals extremely trivial. So you can have just, you have just one index. You take your text, you pass it through the embed model.
            
            This gives you some embeddings. You pass it to your dance, to your vector db. You don't have to do any language identification. Don't have to build different indices. Don't have to do different stemming and stock work. So it's like super easy to build like dense retrieval, 500 languages, which is like completely painful and possible was like Lexile searched.

Cleaned Transcription: Yeah that's definitely hard to debug this. First I would say there's a big need for this. So me as a German speaker, I mean, it's always nice if I go to English, there are like so many models and systems available. But even if you go to German and German, I mean, it's still like a high resource language, has a decent amount of population, it's quite powerful economically, but still the number of things you can get is like really limited and it's like really frustrating to see that in English, you can build these amazing semantic search systems, which works extremely good for Q and A retrieval. But even if you go to German, there's like hardly any models available.
            
            And then if you go further down the the language layer to like more and more low resource languages, it's getting harder and harder to build this. Second motivation is building Multilingual search with lexical search is like really painful. So if you build this in elastic search, for example, you need to know the language.
                        
            So you need to know the language of the document, and for every language you have a different index. Because every language requests a different tokenizer, requires a different stop word list, requires, a different stemmer. So at the end, let's say you want to target, I dunno, European Union with, I dunno, 20 languages.
                        
            You have like 20 different indices in elastic search. Each has a different tokenizer, stemmer, stop word list. . For each document you have to run language identification to see, is it a German document or a French document? And then the big challenge comes at query time. Is it like a German query or a French query or an English query?
                        
            For some really short queries, it's unclear. It can be English and German or French and Spanish. And so how do you query these different indices? Because a Spanish query, you have to add a Spanish index. But with dense retrieval it is extremely trivial. So you can have just one index. You take your text, you pass it through the embedding model.
                        
            This gives you some embeddings. You pass it to your dense, to your vector db. You don't have to do any language identification. Don't have to build different indices. Don't have to do different stemming and stop word list. So it's like super easy to build like dense retrieval, for a 100 languages, which is like completely painful and impossible with Lexical search.

Here is the transcription I need you to clean.

Original Transcription: {original_transcription}
Cleaned Transcription:
```
