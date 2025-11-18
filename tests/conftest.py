# conftest.py
import os
import yaml
import pytest
import allure
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.logger import get_logger

# ---------- Global Logger ----------
framework_logger = get_logger("CONFTEST")

# ---------- Pytest Session Logs ----------
def pytest_sessionstart(session):
    framework_logger.info("******** PYTEST SESSION STARTED ********")

def pytest_sessionfinish(session, exitstatus):
    framework_logger.info(f"******** PYTEST SESSION FINISHED (Status={exitstatus}) ********")

# ---------- Per-Test Lifecycle Logs ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item):
    test_logger = get_logger(item.name)

    test_logger.info(f"========== START TEST: {item.name} ==========")
    outcome = yield
    test_logger.info(f"========== END TEST: {item.name} ==========")

    # Attach log file to Allure
    log_file = f"logs/{item.name}.log"
    try:
        allure.attach.file(
            log_file,
            name=f"Logs - {item.name}",
            attachment_type=allure.attachment_type.TEXT
        )
    except Exception:
        pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    framework_logger.info(f"[SETUP] {item.name}")
    yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    framework_logger.info(f"[CALL] {item.name}")
    yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    framework_logger.info(f"[TEARDOWN] {item.name}")
    yield
    

# -------------------------------------------------
# Load config.yaml
# -------------------------------------------------
@pytest.fixture(scope="session")
def config():
    with open("configs/config.yaml", "r") as conf_file:
        return yaml.safe_load(conf_file)

# -------------------------------------------------
# Playwright instance
# -------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

# -------------------------------------------------
# Browser fixture (headed or headless)
# -------------------------------------------------
@pytest.fixture(scope="session")
def browser(playwright_instance, config):

    browser_name = config.get("browser", "chromium")          # chromium/firefox/webkit
    headed = config.get("headed", True)
    args = config.get("browser_args", ["--start-maximized"])  # Optional future capability

    browser = getattr(playwright_instance, browser_name).launch(
        headless=not headed,
        args=args
    )
    return browser


@pytest.fixture(scope="function")
def context(browser, request):

    test_name = request.node.name

    Path("reports/videos").mkdir(parents=True, exist_ok=True)
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/traces").mkdir(parents=True, exist_ok=True)

    # Enable video only if requested (future capability)
    video_dir = "reports/videos"

    context = browser.new_context(
        record_video_dir=video_dir,
        viewport={"width": 1280, "height": 800}
    )

   # Start tracing
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield context   # Do NOT close before pytest_runtest_makereport

    # Stop trace
    try:
        trace_path = f"reports/traces/{test_name}.zip"
        context.tracing.stop(path=trace_path)
    except Exception as e:
        print(f"[ERROR] Trace stop error: {e}")

    # Close context AFTER attachments
    try:
        context.close()
    except Exception as e:
        print(f"[ERROR] Context close error: {e}")


# -------------------------------------------------
# Page fixture
# -------------------------------------------------
@pytest.fixture(scope="function")
def page(context):
    return context.new_page()

# -------------------------------------------------
# Screenshot + Video + Allure Attachments for FAILED tests
# -------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # Only take screenshot/video for failed tests
    if report.when != "call" or report.passed:
        return

    config = item.funcargs.get("config")
    page = item.funcargs.get("page")

    if not page:
        return

    # Check config flag
    if not config.get("screenshot_on_failure", True):
        return

    test_name = item.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"

    # -------- Screenshot --------
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        allure.attach.file(
            screenshot_path,
            name=f"{test_name}_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")

    # -------- Video --------
    try:
        video = page.video
        if video:
            video_path = video.path()
            allure.attach.file(
                video_path,
                name=f"{test_name}_video",
                attachment_type=allure.attachment_type.MP4
            )
    except Exception as e:
        print(f"[ERROR] Video attachment failed: {e}")
        
    # Only for test execution phase (not setup/teardown)
    if report.when == "call":
        test_name = item.name

        # Log test result
        if report.failed:
            logger.error(f"[FAILED] Test '{test_name}' failed")
            if call.excinfo:
                logger.error(f"Exception: {call.excinfo.value}")
        else:
            logger.info(f"[PASSED] Test '{test_name}' passed")

        # ---------------- Attach log file to Allure ----------------
        log_file = os.path.join("logs", f"run_{datetime.now().strftime('%Y%m%d')}.log")

        if os.path.exists(log_file):
            try:
                allure.attach.file(
                    log_file,
                    name=f"Test Logs - {test_name}",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                print(f"[WARN] Failed to attach log to Allure: {e}")

@pytest.fixture(scope="session")
def logger():
    return get_logger("TestLogger")
   

