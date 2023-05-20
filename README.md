# Super C R A B
Super C R A B is crawling project that will extract the live stream data from the different sites.

![image](https://github.com/Antony-M1/super-crab/assets/96291963/049b7e80-2711-4076-ba32-de84fe7eb723)


### Prerequisites
* [Python 3.10](https://www.python.org/downloads/)
* [mongodb](https://github.com/Antony-M1/mongodb-docker)

# Debugger For VS-Code
This debugger is for `flask` and `scrapy`.
past this below code in `.vscode/launch.json`

```
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": { "FLASK_APP": "app.py", "FLASK_DEBUG": "1" },
      "args": ["run", "--no-debugger", "--no-reload"],
      "jinja": true,
      "justMyCode": true
    },
    {
      "name": "Scrapy",
      "type": "python",
      "request": "launch",
      "module": "scrapy",
      "args": ["runspider", "${file}"],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}

```
