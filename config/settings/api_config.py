from datetime import timedelta
from django.urls import reverse_lazy

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'geniopay.users.api.serializers.UserSerializer',
    'LOGIN_SERIALIZER': 'geniopay.users.api.serializers.MyLoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'geniopay.users.api.serializers.CustomPasswordResetSerializer',
}


REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'geniopay.users.api.serializers.RegisterSerializer',
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    }
}

DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = True
DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER = 'HTTP_X_FORWARDED_FOR'
HTTP_USER_AGENT_HEADER = 'HTTP_USER_AGENT'
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
    "OPTIONS": {
        "min_number": 1500,
        "max_number": 9999
    }
}

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'oauth2_provider.rest_framework.OAuth2Authentication',
        "rest_framework.authentication.TokenAuthentication",
    ),
    'DEFAULT_PARSER_CLASSES': (
        # 'djangorestframework_camel_case.parser.CamelCaseFormParser',
        # 'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        # 'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
        # 'rest_framework_json_api.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework_json_api.schemas.openapi.AutoSchema',
    'SEARCH_PARAM': 'filter[search]',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'core.api.extensions.MyQueryParameterValidationFilter',
        # 'rest_framework_json_api.filters.OrderingFilter',
        # 'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "api_key.permissions.HasAPIKey",
        "rest_framework.permissions.AllowAny",
        "core.api.permissions.APISigningPermission",
        "core.api.permissions.IdempotencyKeyPermission",
    ),
    # "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_PAGINATION_CLASS": 'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    "PAGE_SIZE": 100,

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
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        # 'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # 'core.api.renderers.CustomRenderer',
        # 'rest_framework_json_api.renderers.JSONRenderer',
        # 'rest_framework_json_api.renderers.BrowsableAPIRenderer',
    ],
    'EXCEPTION_HANDLER':
    'core.friendly_errors.handlers.friendly_exception_handler',
    # 'core.api.custom_exception_handler.handle_exception'
    'COMPONENT_SPLIT_REQUEST': True,
    # 'TEST_REQUEST_RENDERER_CLASSES': (
    #     'rest_framework_json_api.renderers.JSONRenderer',
    # ),
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

ALLOWED_VERSIONS = [
    'v1.0', 'v2.0'
]

VERSION_PARAM = 'version'

REST_SAFE_LIST_IPS = [
    '127.0.0.1',
    '123.45.67.89',   # example IP
    '192.168.0.',     # the local subnet, stop typing when subnet is filled out
]

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
        'Api_Key': {
            'type': 'apiKey',
            'description': 'API Keys are issued for specific cases. Contact support for more information.',
            'in': 'header',
            'name': 'X-Auth-Client'
        },
        'Token Authentication': {
            'type': 'apiKey',
            'description': 'If you need to authenticate via bearer auth (e.g., for a cross-origin request), use header `Authorization: Token SMn7BrXSqGmn69mb4GpwRql1Br9KNj` for your API calls. [More info](https://geniopay.docs.apiary.io/#introduction/understanding-authentication)',
            'in': 'header',
            'name': 'Authorization'
        },
        "OAuth 2.0": {
            "type": "oauth2",
            'description': 'This API uses OAuth 2 with the implicit grant flow.Idea for application developers. This will enable users to grant your application access to the GenioPay API on their behalf without the need to manually set up or exchange any keys. [More info](https://geniopay.docs.apiary.io/#introduction/understanding-authentication)',
            "authorizationUrl": "http://oauth2.geniopay.com/authorize",
            "flow": "implicit",
            "scopes": {
                "write": "allows modifying resources",
                "read": "allows reading resources"
            }
        }
    },
    # 'LOGIN_URL': reverse_lazy('account_login'),
    # 'LOGOUT_URL': reverse_lazy('account_logout'),
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
    'DEFAULT_INFO': 'config.admin_api_urls',
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

API_KEY_CUSTOM_HEADER = "HTTP_X_AUTH_CLIENT"
