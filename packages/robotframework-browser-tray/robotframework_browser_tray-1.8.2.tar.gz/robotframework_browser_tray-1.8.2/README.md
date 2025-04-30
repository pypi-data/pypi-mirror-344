# robotframework-browser-tray

Tray icon and REPL for trying out [Browser Library](https://robotframework-browser.org/) keywords using Chromium or Edge


**Requirements**

- NodeJS >= 18
- Windows


## Use Cases

- Execute tests incrementally using e.g. [RobotCode](https://github.com/d-biehl/robotcode)

- Test selectors in an open web page interactively


## How to use it

1. Install the package

```bash
pip install robotframework-browser-tray
```

2. Execute `browser-tray`

**Hint**: In case your environment does not allow executing browser-tray, call the Python module directly:

```bash
python -m BrowserTray
```

3. Click on the tray icon with the Chromium logo

4. Open a Terminal and execute `ibrowser`

**Hint**: In case your environment does not allow executing ibrowser, call the Python module directly:

```bash
python -m BrowserTray.ibrowser
```

### ibrowser

ibrowser allows testing selectors in an open web page interactively. 

To start it execute:

```bash
ibrowser
```

On start up it connects to a running Chromium (started using the tray icon) or Microsoft Edge (see below for instructions).

If you start a new browser while ibrowser is running, call the keyword "Connect" to connect ibrowser to it.

To exit ibrowser press `Ctrl-D`.

### Usage in a Robot Framework Test Suite

Add these lines to the Settings section of the .robot file:

```robotframework
Library       Browser
Test Setup    Connect To Browser    http://localhost:1234    chromium    use_cdp=True
```

In order to use another port execute:

```bash
browser-tray --cdp-port=XXXX
``` 


### Using Microsoft Edge

If Microsoft Edge is installed on your machine:

1. Create a Shortcut to msedge.exe with the target:

```powershell
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=1234 --user-data-dir=C:\Users\YOUR_USER\RFEdgeProfile
```

2. Start Edge using this shortcut

3. Execute `ibrowser`


## How it works

Selecting "Open Chromium" in the tray icon executes `site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium-XX/chrome-win/chrome.exe --remote-debugging-port=1234 --test-type`.

`ibrowser` is a batteries-included [irobot](https://pypi.org/project/robotframework-debug/) that saves time by importing Browser Library and connecting to a running Chromium or Edge.
