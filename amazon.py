from requests_html import HTMLSession

s = HTMLSession()

products = ['B088CZ8CYG', 'B097MQS598',
            'B0B4JTKF6T', 'B0BYNDL5VJ', 'B09SFPJS27', 'B082M7TM9P']

for product in products:

    r = s.get(f'https://www.amazon.sa/-/en/gp/product/{product}/')

    r.html.render(sleep=1)

    price = r.html.find('.a-offscreen')[0].text.replace('SAR', '')
    title = r.html.find('#productTitle')[0].text

    print(f"{title}: Price is .. {price}")
