# ⚙️ TOASTER.EVENT-ROUTING-SERVICE

![drt98l](https://github.com/STALCRAFT-FUNCKA/toaster.event-routing-service/assets/76991612/08409484-c9b2-41f3-9b40-8e43614f0661)

Вся документирующая информация продублированна внутри кода на английском языке.<br>
All documenting information is duplicated within the code in English.<br>


## 📄 Информация ##

**TOASTER.EVENT-ROUTING-SERVICE** - сервис фетчинга событий VK с его Long Polling сервера, преобразования их в более удобные обьекты и маршрутизации на другие сервисы для последующей обработки.

### Входные данные:

**RAW VK event:**

    content type: application\json

    {
        'group_id': 218730916,
        'type': 'message_new',
        'event_id': 'd31e92e8ccde1fa2cde93eeaf9cbdf6d0cd0a936',
        'v': '5.199',
        'object': {
            'message': {
                'date': 1709107598,
                'from_id': 206295116, 
                'id': 0, 'out': 0, 
                'version': 10012065, 
                'attachments': [], 
                'conversation_message_id': 2707, 
                'fwd_messages': [], 
                'important': False, 
                'is_hidden': False, 
                'peer_id': 2000000002, 
                'random_id': 0, 
                'text': 'Hi!', 
                'is_unavailable': True
            }, 
            'client_info': {
                'button_actions': [
                    'text', 
                    'vkpay', 
                    'open_app', 
                    'location', 
                    'open_link', 
                    'callback', 
                    'intent_subscribe', 
                    'intent_unsubscribe'
                    ], 
                'keyboard': True, 
                'inline_keyboard': True, 
                'carousel': True, 
                'lang_id': 0
            }
        }
    }

Пример события, которое приходит от LongPoll сервера на toaster.event-routing-service.

Далее, событие преобразуется в обьект кастомного события, которые выглядят следующим образом в JSON формате:

**MessageEvent:**

    {
        "ts": 1709107923,
        "datetime": "2024-02-28 11:12:03",
        "event_type": "message_new", 
        "event_id": "8dd52b4d7c822b78db23db85bf351c7114e46b36", 
        "user_id": 206295116, 
        "user_name": "Руслан Башинский", 
        "user_nick": "oidaho", 
        "peer_id": 2000000002, 
        "peer_name": "FUNCKA | DEV | CHAT", 
        "chat_id": 2, 
        "cmid": 2708, 
        "text": "Hi!", 
        "reply": null, 
        "forward": [], 
        "attachments": []
    }

**ButtonEvent:**

    {
        "ts": 1709107935, 
        "datetime": "2024-02-28 11:12:15", 
        "event_type": "button_pressed", 
        "event_id": "e93488a3813b59f6c6b53ee51f59103e2a9240d6", 
        "user_id": 206295116, 
        "user_name": "Руслан Башинский", 
        "user_nick": "oidaho", 
        "peer_id": 2000000002, 
        "peer_name": "FUNCKA | DEV | CHAT", 
        "chat_id": 2, 
        "cmid": 2618, 
        "button_event_id": "ac89a3425ec3", 
        "payload": {
            "keyboard_owner_id": 206295116, 
            "call_action": "test"
        }
    }


После исполнения всех преобразований, сервис отправляет событие, в зависимости от некоторых условий, на сервисы обработки соответствующих событий.


### Дополнительно

    docker network
        name: TOASTER
        ip_gateway: 172.18.0.1
        subnet: 172.18.0.0/16
        driver: bridge
    

    docker image
        name: toaster.event-routing-service
        args:
            TOKEN: "..."
            GROUPID: "..."
    

    docker container
        name: toaster.event-routing-service
        network_ip: 172.1.08.5

    docker volumes:
        /var/log/TOASTER/toaster.event-routing-service:/service/logs
        

*Дополнительная информация, которая может пригодиться для поднятия сервиса внутри инфраструктуры.
