# ⚙️ SERVICE.EVENT-FETCHER

![drt98l](https://github.com/STALCRAFT-FUNCKA/toaster.event-routing-service/assets/76991612/08409484-c9b2-41f3-9b40-8e43614f0661)

## 📄 Информация

**SERVICE.EVENT-FETCHER** - сервис фетчинга событий VK с его Long Polling сервера, преобразования их в более удобные обьекты и маршрутизации на другие сервисы через шину Redis для последующей обработки.

### Входные данные

**Пример сырого события VK, которое приходит на service.event-fetcher:**

```shell
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
```

Пример обьект кастомного события, которое готовов к дальнейшей маршрутизации через шину:

```python
class Event:
    event_id: str
    event_type: str

    # Динамически определяемые атрибуты:
    # a. Обязательные атрибуты
    peer: Peer
    user: User

    # b. Возможные атрибуты
    message: Message      # Опрееделяется при типе события "message" и "command"
    button: Button        # Опрееделяется при типе события "button"
    reaction: Reaction    # Опрееделяется при типе события "reaction"
```

Обязательныые атрибуты - атрибуты, которые будут динамически оперделены в любой ситуации.
Данные о пользователе, который спровоцировал событие, и беседе (узле\чате), в которой это событие произошло, будут определены *всегда*. Сервис гарантирует правильность их определения, за исключением случаев, вызванных ошибкой со стороны VK LongPoll сервера.

Возможные атрибуты - атрибуты, которые динамически определяются для обьекта события в зависимости от типа события. Так, например, данные о нажатии кнопки (button) будут отсутствовать в событии "command.

Динамически определяемые атрибуты содержат в себе значения, являющиеся экземплярами классов обьектов (objects), описанных как наследники NamedTuple:

```python
class Button(NamedTuple):
    cmid: int
    beid: str
    payload: dict
```

```python
class Message(NamedTuple):
    cmid: int
    text: str
    reply: Optional[Reply]
    forward: List[Reply]
    attachments: List[str]
```

```python
class Reaction(NamedTuple):
    cmid: int
    rid: int
```

```python
class Reply(NamedTuple):
    cmid: int
    text: str
```

```python
class User(NamedTuple):
    uuid: int
    name: str
    firstname: str
    lastname: str
    nick: str
```

```python
class Peer(NamedTuple):
    bpid: int
    cid: int
    name: str
```

Разумеется, для удобства представления информации и дебага, событие может быть представленно в виде словаря при помощи метода `as_dict()`:

```shell
content type: application\json

{
    'event_type': 'command', 
    'event_id': 'b0d7020c0bd1ad36b76567054400abc8b279f960', 
    'user': {
        'uuid': 206295116, 
        'name': 'Руслан Башинский', 
        'firstname': 'Руслан', 
        'lastname': 'Башинский', 
        'nick': 'oidaho'
    }, 
    'peer': {
        'bpid': 2000000002, 
        'cid': 2, 
        'name': 'FUNCKA | TOASTER | DEV | CHAT'
    }, 
    'message': {
        'cmid': 3895, 
        'text': '/command', 
        'reply': None, 
        'forward': [], 
        'attachments': []
    }
}
```

### Дополнительно

Docker setup:

```shell
docker network
    name: TOASTER
    ip_gateway: 172.18.0.1
    subnet: 172.18.0.0/24
    driver: bridge


docker image
    name: toaster.event-routing-service
    args:
        TOKEN: "..."
        GROUPID: "..."


docker container
    name: toaster.event-routing-service
    network_ip: 172.18.0.5
```

Jenkins shell command:

```shell
imageName="service.event-fetcher"
containerName="service.event-fetcher"
localIP="172.18.0.5"
networkName="TOASTER"

#stop and remove old container
docker stop $containerName || true && docker rm -f $containerName || true

#remove old image
docker image rm $imageName || true

#build new image
docker build . -t $imageName \
--build-arg TOKEN=$TOKEN \
--build-arg GROUPID=$GROUPID 

#run container
docker run -d \
--name $containerName \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
