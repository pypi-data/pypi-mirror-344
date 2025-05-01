READ_SCOPE = "read"
WRITE_SCOPE = "write"

ALL_SCOPES = [READ_SCOPE, WRITE_SCOPE]

GET_METHOD = "get"
POST_METHOD = "post"
PATCH_METHOD = "patch"

READ_METHODS = [GET_METHOD]
WRITE_METHODS = [POST_METHOD, PATCH_METHOD]
ALL_METHODS = [GET_METHOD, POST_METHOD, PATCH_METHOD]

SCOPE_TO_METHODS = {
    READ_SCOPE: READ_METHODS,
    WRITE_SCOPE: WRITE_METHODS
}

EXCLUDED_PARAMETERS = ["include_deleted_data", "include_remote_data", "include_shell_data"]

# TAG RELATED CONSTANTS
IRREGULAR_TAG_MAP = {
    "RemoteUser": "users",
    "Opportunity": "opportunities"
}
SINGULAR_TAGS = {"time-off", "bank-info"}