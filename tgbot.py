
import telebot
from selenium import webdriver
from bs4 import BeautifulSoup

# set up the Selenium driver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# create a new Telegram bot
bot = telebot.TeleBot("6286727561:AAFNsjVx8ptLFDDdBxvzswm_Or-wgaTmiUM")

# define the command handlers
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hello! Welcome to the video downloader bot. Use the /info command to get more information.")

@bot.message_handler(commands=["info"])
def send_info(message):
    bot.reply_to(message, "To use this bot, send a message with a video link.")

@bot.message_handler(commands=["status"])
def send_status(message):
    bot.reply_to(message, "The bot is currently running.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    driver.get(url)

    # get the page source using Selenium
    html = driver.page_source

    # parse the HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # find the <script> tag with the desired content
    script_tag = soup.find("script", string=lambda x: "evideo_vkey" in str(x))

    # extract the value of the evideo_vkey variable from the script tag
    evideo_vkey = None
    if script_tag:
        script_text = script_tag.string
        if script_text:
            evideo_vkey_index = script_text.find("evideo_vkey")
            if evideo_vkey_index >= 0:
                evideo_vkey_start = script_text.find('"', evideo_vkey_index)
                evideo_vkey_end = script_text.find('"', evideo_vkey_start + 1)
                evideo_vkey = script_text[evideo_vkey_start + 1 : evideo_vkey_end]

    # download link
    name=evideo_vkey
    tmp=name.find('theync')
    if(tmp!=-1):
        a=name.split("com/")
        b=a[0].replace('thumbs','media')
        c=a[1].replace('thumbs','videos')
        e='com/'
        d=b+e+c
        d=''.join(d)
        tmp1=d.find('.mp4')
        if(tmp1!=-1):
            f='.mp4'
            g=d.split(".mp4/")
            h=g[0]+f
            bot.reply_to(message, h)
        else:
            x='.avi'
            g=d.split(".avi/")
            h=g[0]+x
            bot.reply_to(message, h)
    else:
        a='https://www.xrares.com/vsrc/iphone/'
        b='https://www.xrares.com/vsrc/h264/'
        c='/HD'
        d=a+name
        e=b+name+c
        bot.reply_to(message, f"Download link for iPhone: {d}")
        bot.reply_to(message, f"Download link for h264: {e}")

# start the bot
bot.polling()
