from requests import get
from datetime import date, datetime
from discord import Embed

from ...environment import bot_environment

async def weather_command(context, city):
    weather_json = get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric&lang=pl'.format(city, bot_environment.weather_token)).json()

    if weather_json['cod'] != 200:
        return

    # Create Rich Embed with received weather.
    embed = Embed(
        title='{} - {}'.format(city.title(), date.today().strftime("%d %B %Y")),
        type='rich',
    )

    # Set thumbnail and footer with openweathermap data.
    embed.set_thumbnail(url='https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/widgets/{}.png'.format(weather_json['weather'][0]['icon']))
    embed.set_footer(text='openweathermap.org')

    # Add field with wind speed
    wind_speed = '{0:.1f}'.format(weather_json["wind"]["speed"] * 3.6)
    embed.add_field(
        name=':dash: Wind speed',
        value=f'{wind_speed} km/h',
        inline=True,
    )

    # Add field with cloudiness
    embed.add_field(
        name=':white_sun_cloud: Cloudiness',
        value=f'{weather_json["clouds"]["all"]}%',
        inline=True,
    )

    # Add field with humidity
    embed.add_field(
        name=':droplet: Humidity',
        value=f'{weather_json["main"]["humidity"]}%',
        inline=True,
    )

    # Add field with pressure
    embed.add_field(
        name=':compression: Pressure',
        value=f'{weather_json["main"]["pressure"]} hPa',
        inline=True,
    )

    # Add field with Sunrise time
    sunrise_time = datetime.fromtimestamp(weather_json["sys"]["sunrise"]).strftime("%H:%M")
    embed.add_field(
        name=':sunrise: Sunrise',
        value=sunrise_time,
        inline=True,
    )

    # Add field with Sunset time
    sunset_time = datetime.fromtimestamp(weather_json["sys"]["sunset"]).strftime("%H:%M")
    embed.add_field(
        name=':city_sunset: Sunset',
        value=sunset_time,
        inline=True,
    )

    # Add field with Max Temp
    embed.add_field(
        name=':sunny: Max Temperature',
        value=f'{weather_json["main"]["temp_max"]}°C',
        inline=True,
    )

    # Add field with Min Temp
    embed.add_field(
        name=':cloud: Min Temperature',
        value=f'{weather_json["main"]["temp_min"]}°C',
        inline=True,
    )

    # Add field with Temp
    embed.add_field(
        name=':thermometer: Temperature',
        value=f'{weather_json["main"]["temp"]}°C',
        inline=True,
    )

    # Add field with Feels Like temp
    embed.add_field(
        name=':cold_face: Feels Like',
        value=f'{weather_json["main"]["feels_like"]}°C',
        inline=True,
    )

    await context.send(embed=embed)
