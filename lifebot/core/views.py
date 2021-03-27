import urllib3, telepot

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url,
        num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager,
    dict(proxy_url=proxy_url, num_pools=1,
    maxsize=1, retries=False, timeout=30))

secret = "f36ab0c8-d564-40a5-9f6b-4a18820b7513"
bot = telepot.Bot('1746290681:AAGqISC4M37Fsy6Cq1TNgTKOeG0YJVPUWQ4')
bot.setWebhook("https://armanahdi.pythonanywhere.com/{}".format(secret),
    max_connections=1)


def telegram_webhook(request):
    update = request['POST']
    print('-------------new hook-----------------')
    if "message" in update:
        print('-------------new message-----------------')
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            try:
                #reply = text_replier(text, update["message"]["chat"])
                bot.sendMessage(chat_id, 'hello')
            except Exception as e:
                bot.sendMessage(chat_id, f"Something wrong happend! Please forward this message to @MrArmanHadi:\n{e}")
        else:
            bot.sendMessage(chat_id, "ببین یه چیزی بهت میگما!")
