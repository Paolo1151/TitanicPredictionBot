# Establish a Connection (AKA Logging In)
from decouple import config

import pandas as pd

from discord.ext import commands
import joblib

TOKEN = config('DISCORD_TOKEN')
GUILD = config('DISCORD_GUILD')
PREFIX = 'T>'

## Defining Bot Class

class TitanicBot(commands.Bot):
    async def on_ready(self):
        self.model = joblib.load('objects/model.joblib')
        print(f'{self.user} has connected to Discord!')

    def model_predict(self, data): 
        return self.model.predict(data)

## Defining Instance

bot = TitanicBot(command_prefix=PREFIX)

## Defining the Commands 

@bot.command()
async def predict(ctx, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked):
    data = pd.DataFrame(
        {'Pclass': pclass,
        'Name': name,
        'Sex': sex,
        'Age': age,
        'SibSp': sibsp,
        'Parch': parch,
        'Ticket': ticket,
        'Fare': fare,
        'Cabin': cabin,
        'Embarked': embarked},
    index=[0])

    for idx, dtype in enumerate([int, str, str, float, int, int, str, float, str, str]):
        data.iloc[0,idx] = dtype(data.iloc[0,idx])

    prediction = bot.model_predict(data)

    await ctx.send('Survived!' if prediction[0] == 1 else 'Died!')

bot.run(TOKEN)