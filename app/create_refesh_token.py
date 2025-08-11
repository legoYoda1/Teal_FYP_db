from dropbox import DropboxOAuth2FlowNoRedirect

auth_flow = DropboxOAuth2FlowNoRedirect(
    "ihi1pgsqjt1bv4p",
    "8etywhdww8smmy3",
    token_access_type="offline"
)

auth_url = auth_flow.start()
print("Visit this URL and approve:", auth_url)
auth_code = input("Enter the auth code here: ").strip()

result = auth_flow.finish(auth_code)
print("Refresh Token:", result.refresh_token)