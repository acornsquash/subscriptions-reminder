
Python bot to remind the user to cancel subscriptions. requires installing poetry.

For privacy, the subscriptions.json exists locally on your machine. To use the email send feature rather than just printing to the terminal, make a .env file that looks like env.example here. For gmail, generate an app password. To generate a Google App Password, first ensure that 2-Step Verification is enabled on your Google Account, then go to the Google Account security page, find the "App passwords" option, select the specific app and device (or enter a custom name), and click "Generate" to create the 16-digit password. 

to add or change a subscription
poetry run subscriptions add “Hulu” --cost 18.99 --renewal 2025-08-27 --interval monthly

to run the program 
poetry run subscriptions daily


