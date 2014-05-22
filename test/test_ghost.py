from ghost import Ghost
ghost = Ghost()
ghost.set_proxy("HTTP")
page, extra_resources = ghost.open("http://www.singaporeair.com/SAA-flow.form")
print page.http_status
print ghost.content(False)