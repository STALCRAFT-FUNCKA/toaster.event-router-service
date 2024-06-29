# ⚙️ TOASTER.EVENT-ROUTING-SERVICE

![drt98l](https://github.com/STALCRAFT-FUNCKA/toaster.event-routing-service/assets/76991612/08409484-c9b2-41f3-9b40-8e43614f0661)

## 📄 Информация ##

**TOASTER.EVENT-ROUTING-SERVICE** - сервис фетчинга событий VK с его Long Polling сервера, преобразования их в более удобные обьекты и маршрутизации на другие сервисы для последующей обработки.

### Входные данные

**RAW VK event:**

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

Пример события, которое приходит от LongPoll сервера на toaster.event-routing-service.

Далее, событие преобразуется в обьект кастомного события, которые выглядят следующим образом:

**Event**

```python
class Event(object):
    event_id: str = None
    event_type: str = None

    # Динамически определяемые атрибуты:
    # a. Обязательные атрибуты
    peer: Peer
    user: User

    # b. Возможные атрибуты
    message: Message
    button: Button
    reaction: Reaction
```

Обязательныые атрибуты - атрибуты, которые будут динамически оперделены в любой ситуации.
Данный о бользователе, который спровоцировал события, и беседе(узле\чате), в котором это событие произошло, будут определены всегда. Сервис гарантирует правильность их ппределения, за исключением случаев, вызванных ошибкой со стороны самого LongPoll сервера.

Возможные атрибуты - атрибуты, которые определяются для класса события в зависимости от типа события. Так, например, данные о нажатии кнопки (Button) будут отсутствовать в событии команды.

Динамически определяемые атрибуты содержат в себе значения, являющиеся экземплярами классов обьектов, описанных как наследники NamedTuple:

**Button**

```python
class Button(NamedTuple):
    cmid: int
    beid: str
    payload: dict
```

**Message**

```python
class Message(NamedTuple):
    cmid: int
    text: str
    reply: Optional[Reply]
    forward: List[Reply]
    attachments: List[str]
```

**Reaction**

```python
class Reaction(NamedTuple):
    cmid: int
    rid: int
```

**Reply**

```python
class Reply(NamedTuple):
    cmid: int
    text: str
```

**User**

```python
class User(NamedTuple):
    uuid: int
    name: str
    firstname: str
    lastname: str
    nick: str
```

**Peer**

```python
class Peer(NamedTuple):
    bpid: int
    cid: int
    name: str
```

Разумеется, для удобства представления информации и дебага, событие может быть представленно как dict объект при помощи метода `as_dict()`:

**Event.as_dict()**

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

После исполнения всех преобразований, сервис отправляет событие, в зависимости от некоторых условий, на сервисы обработки соответствующих событий.

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
imageName="toaster.event-routing-service"
containerName="toaster.event-routing-service"
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
