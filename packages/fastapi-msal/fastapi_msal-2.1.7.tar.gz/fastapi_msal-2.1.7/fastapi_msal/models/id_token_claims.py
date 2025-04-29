import json
import time
from enum import Enum
from typing import Optional, Union

from msal.oauth2cli import oidc
from pydantic import BaseModel, Field, PrivateAttr

from fastapi_msal.core import OptStr, OptStrsDict

from .base_auth_model import BaseAuthModel
from .user_info import UserInfo


class TokenStatus(Enum):
    """
    The validateion status of a token.
    https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation
    """

    UNKNOWN = "The token status is unknown."
    """
    The status of the token is unknown.
    """

    VALID = "The token is valid."
    """
    The token is valid.
    """

    NOT_YET_VALID = "The token is not yet valid."
    """
    nbf is optional per JWT specs
    This is not an ID token validation, but a JWT validation
    https://tools.ietf.org/html/rfc7519#section-4.1.5
    """

    WRONG_ISSUER = "The token issuer does not match the expected issuer."
    """
    https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationResponse
    The Issuer Identifier for the OpenID Provider (which is typically obtained during Discovery),
    MUST exactly match the value of the iss (issuer) Claim.
    """

    WRONG_AUDIANCE = "The token audiance does not contain the client_id."
    """
    The aud (audience) claim must contain this client's client_id
    case-sensitively. Was your client_id in wrong casing?
    """

    EXPIRED = "The token has already expired."
    """
    The ID token already expires.
    """

    WRONG_NONCE = "The token nonce does not match the expected nonce."
    """
    Nonce must be the same value as the one that was sent in the Authentication Request.
    """


class AADInternalClaims(BaseModel):
    aio: OptStr = None
    """
    An internal claim used by Azure AD to record data for token reuse. Resources should not use this claim.
    """

    rh: OptStr = None
    """
    An internal claim used by Azure to revalidate tokens. Resources should not use this claim.
    """

    uti: OptStr = None
    """
    Token identifier claim, equivalent to jti in the JWT specification. Unique,
     per-token identifier that is case-sensitive.
    """


class IDTokenClaims(UserInfo, AADInternalClaims, BaseAuthModel):
    """
    The ID token is a security token that contains claims about the authentication of an end-user by
      an authorization server, when using a client, and potentially other requested claims.
    The ID token is represented as a JSON Web Token (JWT).
    For more information: https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference
    """

    audience: Union[OptStr, list[str]] = Field(None, alias="aud")
    """
    An audience claim identifies the intended recipient of the token.
    For Azure AD B2C, the audience is your app's Application ID, as assigned to your app in the app registration portal.
    Your app should validate this value and reject the token if it does not match.
    """

    issuer: OptStr = Field(None, alias="iss")
    """
    This claim identifies the fastpi_msal token service (STS) that constructs and returns the token.
    It also identifies the Azure AD directory in which the user was authenticated.
    Your app should validate the issuer claim to ensure that the token came from the v2.0 endpoint.
    It also should use the GUID portion of the claim to restrict the set of tenants that can sign in to the app.
    """

    issue_time: Optional[float] = Field(None, alias="iat")
    """
    The time at which the token was issued, represented in epoch time.
    """

    identity_provider: OptStr = Field(None, alias="idp")
    """
    Records the identity provider that authenticated the subject of the token.
    This value is identical to the value of the issuer claim unless the user account isn't in the same tenant-
     as the issuer - guests, for instance.
    If the claim isn't present, it means that the value of iss can be used instead.
    For personal accounts being used in an organizational context (for instance, a personal account invited to a tenant),
    the idp claim may be 'live.com' or an STS URI containing the Microsoft account tenant-
     9188040d-6c67-4c5b-b112-36a304b66dad.
    """

    not_before: Optional[float] = Field(time.time() - 1, alias="nbf")
    """
    This claim is the time at which the token becomes valid, represented in epoch time.
    This is usually the same as the time the token was issued.
    Your app should use this claim to verify the validity of the token lifetime.
    """

    exp: Optional[float] = None
    """
    The expiration time claim is the time at which the token becomes invalid, represented in epoch time.
    Your app should use this claim to verify the validity of the token lifetime.
    """

    code_hash: OptStr = Field(None, alias="c_hash")
    """
    The code hash is included in ID tokens only when the ID token is issued with an OAuth 2.0 authorization code.
    It can be used to validate the authenticity of an authorization code. To understand how to do this validation,
    see the OpenID Connect specification: https://openid.net/specs/openid-connect-core-1_0.html#HybridIDToken

    This claim isn't returned on ID tokens from the /token endpoint.
    """

    access_token_hash: OptStr = Field(None, alias="at_hash")
    """
    The access token hash is included in ID tokens only when the ID token is issued from the /authorize endpoint
     with an OAuth 2.0 access token.
    It can be used to validate the authenticity of an access token.
    To understand how to do this validation, see the OpenID Connect specification.
    https://openid.net/specs/openid-connect-core-1_0.html#HybridIDToken

    This claim isn't returned on ID tokens from the /token endpoint.
    """

    nonce: OptStr = None
    """
    A nonce is a strategy used to mitigate token replay attacks.
    Your app can specify a nonce in an authorization request by using the nonce query parameter.
    The value you provide in the request will be emitted unmodified in the nonce claim of an ID token only.
    This allows your app to verify the value against the value it specified on the request,
    which associates the app's session with a given ID token.
    Your app should perform this validation during the ID token validation process.
    """

    subject: OptStr = Field(None, alias="sub")
    """
    This is the principal about which the token asserts information, such as the user of an app.
    This value is immutable and cannot be reassigned or reused.
    It can be used to perform authorization checks safely, such as when the token is used to access a resource.
    By default, the subject claim is populated with the object ID of the user in the directory.
    To learn more: https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-token-session-sso
    """

    tenant_id: OptStr = Field(None, alias="tid")
    """
    Represents the tenant that the user is signing in to.
    For work and school accounts, the GUID is the immutable tenant ID of the organization that the user is signing in to.
    For sign-ins to the personal Microsoft account tenant (services like Xbox, Teams for Life, or Outlook),
     the value is 9188040d-6c67-4c5b-b112-36a304b66dad.
    """

    ver: OptStr = None
    """
    Indicates the version of the token.
    """

    #### Review the below claims if still needed

    auth_time: Optional[float] = None
    """
    This claim is the time at which a user last entered credentials, represented in epoch time.
    """

    msal_policy: OptStr = Field(None, alias="tfp")
    """
    This is the name of the policy that was used to acquire the token.
    """

    ### Private attributes

    _id_token: Optional[str] = PrivateAttr(None)
    """
    The raw id_token that was used to create this object - private attribute for internal use only
    Will be set only via the `decode_id_token` method
    """

    @staticmethod
    def decode_id_token(id_token: str) -> Optional["IDTokenClaims"]:
        decoded: OptStrsDict = json.loads(oidc.decode_part(id_token.split(".")[1]))
        if decoded:
            token_claims = IDTokenClaims.model_validate(decoded)
            token_claims._id_token = id_token
            return token_claims
        return None

    def validate_token(
        self, client_id: OptStr = None, issuer: OptStr = None, nonce: OptStr = None, now: Optional[float] = None
    ) -> TokenStatus:
        token_status = TokenStatus.VALID
        _now = int(now or time.time())
        skew = 120  # 2 minutes
        if self.not_before and _now + skew < self.not_before:
            token_status = TokenStatus.NOT_YET_VALID
        if issuer and issuer != self.issuer:
            token_status = TokenStatus.WRONG_ISSUER
        if client_id:
            valid_aud = client_id in self.audience if isinstance(self.audience, list) else client_id == self.audience
            if not valid_aud:
                token_status = TokenStatus.WRONG_AUDIANCE
        if self.exp and _now - skew > self.exp:
            token_status = TokenStatus.EXPIRED
        if nonce and nonce != self.nonce:
            token_status = TokenStatus.WRONG_NONCE
        return token_status
