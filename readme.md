A simple proof of concept ETL Pipeline to take posts from an italian messageboard and translate them into various languages. 
The original author of wait-for-it.sh is vishnubob found here https://github.com/vishnubob/wait-for-it


Q&A: 


Q:How do I add or remove a language from the translation API? 
A:Simply add the language code to the list in the docker compose file.  A List of supported languages is found in the libretranslate API https://libretranslate.com/docs/#/translate/post_languages here . 


Q: How do I select how many pages the program scrapes?
A: Change the variable PAGES within the scraper entry. 


Q: Why does the startup take so long? 
A: Libretranslate needs to download the language models on startup. There may be a way to skip this however i have not been able to make it work with the libretranslate documentation. I apologize. 


Q: How Do I run the Program? 
A: Simply run the runme.bat on windows. 

Q:How can I access the scraped Information?
A:Given that you don't change anything of note under localhost/docs for the simple FASTAPI GUI
