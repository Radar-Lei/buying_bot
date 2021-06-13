import asyncio
from pyppeteer import launch
import schedule
import time

async def loop_shooter(page,product_url,item_num,t_out,t_out_page):
    try:
        await page.goto(product_url,timeout=t_out_page)
        cart_count = await page.waitForSelector('span[class="cart-products-count"]',timeout=t_out)
        cart_count_num = await page.evaluate('(element) => element.textContent', cart_count)
        if cart_count_num == '(0)':
            await page.evaluate(f"""() => {{
                document.getElementById('quantity_wanted').value = '{item_num}';
            }}""")

            add_to_cart = await page.waitForSelector('button[class="btn btn-primary add-to-cart"]',timeout=t_out)
            await page.evaluate('(element) => element.click()', add_to_cart)
            resume_to_cart = await page.waitForSelector('a[href="//www.dxpool.io/index.php?controller=cart&action=show"]',timeout=t_out)
            await page.evaluate('(element) => element.click()', resume_to_cart)
        else:
            await page.goto('https://www.dxpool.io/index.php?controller=cart&action=show')

        resume_to_order = await page.querySelector('a[class="btn btn-primary"]')
        while not resume_to_order:
            print("没有货")
            time.sleep(1)
            await page.reload()
            resume_to_order = await page.querySelector('a[class="btn btn-primary"]')

        await page.evaluate('(element) => element.click()', resume_to_order)



        confirm_address = await page.waitForSelector('button[name="confirm-addresses"]',timeout=t_out)
        try:
            await page.evaluate('(element) => element.click()', confirm_address)
        except:
            print('1')

        confirm_delivery = await page.waitForSelector('button[name="confirmDeliveryOption"]',timeout=t_out)
        try:
            await page.evaluate('(element) => element.click()', confirm_delivery)
        except:
            print('2')



        payment_op_1 = await page.waitForSelector('input[id="payment-option-1"]',timeout=t_out)
        await page.evaluate('(element_1) => element_1.click()', payment_op_1)
        approval = await page.waitForSelector('input[id="conditions_to_approve[terms-and-conditions]"]',timeout=t_out)
        await page.evaluate('(element_2) => element_2.click()', approval)


        final_confirm = await page.waitForSelector('button[class="btn btn-primary center-block"]', timeout=t_out)
        await page.evaluate('(element_2) => element_2.click()', final_confirm)


        await asyncio.sleep(10000)
    except:
        # the bot restarts whenever there's an error
        await loop_shooter(page,product_url,item_num,t_out,t_out_page)


async def main():
    """

    """
    item_num = 1
    product_url = 'https://www.dxpool.io/index.php?id_product=62&rewrite=mini-doge&controller=product'
    # maximum time for waitForSelector, throw error when reaching timeout. unit: ms.
    t_out = 1500
    # maximum time for page.goto. timeout for refresh the page
    t_out_page = 3000
    # '--no sandbox' for running the code in ubuntu, '--disable-infobars' for avoiding webdriver detection
    browser = await launch(headless=False, userDataDir='./userdata', args=['--disable-infobars', '--no-sandbox'])
    page = await browser.newPage()
    # change user profile, default 0. 1 means that you want to change login info.
    change_or_not = 0
    if change_or_not == 1:
        # stay in the current page. unit: s
        await asyncio.sleep(10000)

    await loop_shooter(page,product_url,item_num,t_out,t_out_page)

def syncfunc():
    asyncio.get_event_loop().run_until_complete(main())

schedule.every().day.at("13:33").do(syncfunc)

# while True is necessary for keeping schedule module running in the background. e.g. every 10 mins we run our code.
while True:
    schedule.run_pending()
    time.sleep(1)
