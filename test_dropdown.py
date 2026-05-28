import asyncio
from playwright.async_api import async_playwright
from robots.clinux import login_clinux

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        if await login_clinux(page):
            await page.wait_for_timeout(5000)
            elem = page.locator('/html/body/div[1]/div[4]/div/div[7]')
            if await elem.count():
                print('XPath funciona!')
                await elem.click()
                await page.wait_for_timeout(1000)
                await page.click('//div[@class="v-list-item__title" and text()="Todos"]')
                print('Todos clicado!')
            else:
                print('XPath não encontrado')
        await browser.close()
asyncio.run(test())
