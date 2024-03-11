import requests
WB_CARD_API_URL="https://card.wb.ru/cards/v1/detail"
# WB_CARD_API_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
wb_api_url_params = {
    "appType": 1,
    "curr": "rub",
    "dest": -1257786,
    "spp": 30,
    "nm": "{article}"
}

def find(article):
    wb_api_url_params["nm"].format(article=article)
    wb_response = requests.get(
        url=WB_CARD_API_URL,
    params=wb_api_url_params
    )
    print(wb_response)
    print(wb_response.url)
    print(wb_response.content)


# def find(article):
#     wb_response = requests.get(
#         url=WB_CARD_API_URL.format(article=article))
#     print(wb_response)
#     print(wb_response.content)

find(int(input()))
