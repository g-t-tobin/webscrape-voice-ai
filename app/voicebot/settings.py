import os
SECRET_KEY = os.getenv("SECRET_KEY")

ROOT_URLCONF = 'voicebot.urls'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += [
    'channels',
    'bot',  # your app name
]
ASGI_APPLICATION = 'voicebot.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add custom template dirs here
        'APP_DIRS': True,  # ✅ this is what makes Django look inside app/templates/
        'OPTIONS': {
           'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]
        },
    },
]

