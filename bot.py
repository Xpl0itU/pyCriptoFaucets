import asyncio
import datetime
import pyppeteer
from dotenv import load_dotenv
import os

load_dotenv()

loopError = False
WEBSITES_FS = "config/websites.txt"
date = datetime.datetime.now().strftime("%X %b %d")

async def main():
    email = os.environ['EMAIL']
    passw = os.environ['PASS']
    print("🦾 ----------------- BOT STARTING ----------------- 🦾")
    print("Use email:", email)
    print("\n  🍀 Good Luck!\n")
    webs = open(WEBSITES_FS, "r")
    websitesFs = webs.read()
    websites = [s.removesuffix(",") + '/set-language/en' for s in websitesFs.splitlines()]
    global loopError
    while True:
        print(date + "\n----------------- ATTEMPTING ROLLS -----------------")
        browser = await pyppeteer.launch(headless=True, args="--lang=en")
        page = await browser.newPage()
        await page.setViewport({'width': 1866, 'height': 768})
        for faucet in websites:
            try:
                await page.goto(faucet, waitUntil="networkidle2", timeout=0)
                await asyncio.sleep(0.2)
                print("\n" + faucet)
                await page.type('input[name=email]', email, delay=20)
                await page.type('input[name=password]', passw, delay=20)
                element = await page.xpath('//button[contains(text(), "LOGIN!")]')
                await element[0].click()
                await page.waitForNavigation(waitUntil="networkidle2", timeout=0)
                element_roll = await page.xpath('//button[contains(text(), "ROLL!")]')
                await element_roll[0].click()
                await asyncio.sleep(2)
                innerText = await page.evaluate('''() => document.querySelector('.navbar-coins').innerText''')
                print("Balance 🏛️ -> ", innerText)
                print("👍 SUCCESS! Coin claimed!")
            except Exception as e:
                loopError = True
                print("Error was encountered on: " + faucet)
                print("Error: ", e)
                print("👎 FAIL. Coin not claimed. ❌\n\n")
        if loopError:
            loopError = False
            print(date + "There was an error, retrying in 10 mins")
            await asyncio.sleep(600)
        else:
            print("🏆 All coins have been collected successfully! Well job")
            print(date + "\nGoing to sleep\n   See you in one hour 💤")
            await asyncio.sleep(3700)

asyncio.run(main())
