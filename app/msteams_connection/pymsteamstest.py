import pymsteams

my_teams_message = pymsteams.connectorcard("https://imecinternational.webhook.office.com/webhookb2/27bf236c-227a-4ac1-ba5c-d1480181af65@a72d5a72-25ee-40f0-9bd1-067cb5b770d4/IncomingWebhook/d303c45f233f4288bb5dc22b2f8eafe7/de41a3d0-81c7-479d-8b2a-c63812604213")

my_teams_message.text("Hello world from python script")

my_teams_message.printme()
