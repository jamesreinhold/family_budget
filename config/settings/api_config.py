from datetime import timedelta
from django.urls import reverse_lazy


HTTP_USER_AGENT_HEADER = 'HTTP_USER_AGENT'


# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        'rest_framework.authentication.BasicAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    
    'SEARCH_PARAM': 'filter[search]',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "api_key.permissions.HasAPIKey",
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.LimitOffsetPagination',
    "PAGE_SIZE": 2,

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '1000/day'
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'COMPONENT_SPLIT_REQUEST': True,
}

ALLOWED_VERSIONS = [
    'v1.0', 'v2.0'
]

VERSION_PARAM = 'version'


SWAGGER_SETTINGS = {
    "SUPPORTED_SUBMIT_METHODS": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'destroy',
        'head',
        'delete'
    ],
    'SECURITY_DEFINITIONS': {
        'Token Authentication': {
            'type': 'apiKey',
            'description': 'If you need to authenticate via bearer auth (e.g., for a cross-origin request), use header `Authorization: Token SMn7BrXSqGmn69mb4GpwRql1Br9KNj` for your API calls. [More info](https://geniopay.docs.apiary.io/#introduction/understanding-authentication)',
            'in': 'header',
            'name': 'Authorization'
        },
    },
    'LOGIN_URL': reverse_lazy('account_login'),
    'LOGOUT_URL': reverse_lazy('account_logout'),
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'DOC_EXPANSION': 'none',  # ["list"*, "full", "none"]
    'REFETCH_SCHEMA_ON_LOGOUT': True,
    'SHOW_REQUEST_HEADERS': True,
    'APIS_SORTER': 'alpha',
    'DEFAULT_MODEL_DEPTH': 3,  # -1
    'DEFAULT_MODEL_RENDERING': 'example',
    'OPERATIONS_SORTER': 'None',  # [alpha, method, none],
    'TAGS_SORTER': 'alpha',
    'DEEP_LINKING': True,
    'DISPLAY_OPERATION_ID': True,
    'PERSIST_AUTHORIZATION': True,
    # 'SUPPORTED_SUBMIT_METHODS': "[\"get\", \"post\"]",
    'TRY_IT_OUT_ENABLED': True,
    'FILTER': True,
    'WITH_CREDENTIALS': True,
    'PERSIST_AUTHORIZATION': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'HIDE_HOSTNAME': False,
    'PATH_IN_MIDDLE': False,
    'REQUIRED_PROPS_FIRST': True
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': True,
    'PATH_IN_MIDDLE': True
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': "cRcpzLRunm5WJt9mRnLySoPdoM2mjFlRcuSOFbB8xOo9kLxW1JQDrT98EjLBQGfh",
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer', ),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'profile_id',
    'USER_AUTHENTICATION_RULE': 'core.api.extensions.custom_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
JWT_RETURN_EXPIRATION = True
