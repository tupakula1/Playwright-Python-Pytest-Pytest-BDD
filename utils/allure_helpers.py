import allure

def attach_screenshot(page, name="Screenshot"):
    screenshot = page.screenshot()
    allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)

def attach_console_logs(page):
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))
    allure.attach("\n".join(logs), "Console Logs", allure.attachment_type.TEXT)
