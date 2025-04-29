import uuid
import ServexTools.Tools as Tools
from flask_socketio import SocketIO


_socketio_instance = None

# Forma recomendada: usar URL explícita para Redis
REDIS_URL = 'redis://localhost:6379/0'  # Puedes parametrizar esto con variables de entorno

def get_socketio():
    global _socketio_instance
    return _socketio_instance

def init_socketio(app,isProduccion=False,Proyecto="Servex",usarGevent=True):
    global _socketio_instance
    if _socketio_instance is None:
        if not Tools.ExistFile('sctkRedis'):
            Tools.CreateFile(nombre="sctkRedis",datos=uuid.uuid4().hex)
        
        canalredis = Tools.ReadFile("sctkRedis")
        if isProduccion:
            if usarGevent:
                from gevent import monkey
                monkey.patch_all()
            _socketio_instance = SocketIO(app,
                            ping_timeout=25000,
                            ping_interval=10000,
                            cors_allowed_origins="*",
                            async_mode='gevent',
                            message_queue=REDIS_URL,  # <--- URL explícita
                            channel=Proyecto + canalredis,
                            logger=False,
                            engineio_logger=False)
        else:
            _socketio_instance = SocketIO(app,
                        ping_timeout=5000,
                        ping_interval=2000,
                        cors_allowed_origins="*",
                        async_mode='threading')
    return _socketio_instance

# Nota: Puedes usar variables de entorno para REDIS_URL en producción para mayor flexibilidad y seguridad.
