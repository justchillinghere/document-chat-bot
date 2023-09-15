1. Functional requirements for bot commands:

   - /start – Starts the bot and shows the greeting
   - /help – Shows the list of available commands
   - /stop – Stops the bot

   - /file – accepts the file and parse its contents in langchain
   - /lang – shows the list of supported languages
   - /question – accepts a question for the downloaded pdf file. Responds with information from the pdf
   - /end_conversation – ends conversation with the file

2. Rules of usage:
   - After the start the user information is saved in the database
   - When user uploads file, the program stores the embedigns of the user in the database until next file upload or bot stop
   - The maximum file size is 5 Mb now
   - Now only english version is supported (for stability)
