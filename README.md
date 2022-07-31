# wsm - websocket messaging

a idfk messaging program using (web)sockets

**`src` folder contains:**
 - `client`; python commandline client
 - `server`; python chat server
 - `webclient`; html + css + js GUI client
 - `webserver`; python webserver to serve the webclient html

the three run_*.py files runs each of the three python scripts respectively, with optional commandline arguments (positional):
 - `run_client`: `[uri]` (uri of the server to connect to, i.e. ws://ip:port) 
 - `run_server`: `[port]` (port to listen for connections on; clients must connect to this)
 - `run_webserver`: `[websocket ip]` `[websocket port]` `[webserver port]` (external ip and port of chat server the webclient tries to connect to, port of webserver to listen on... 80 to access directly in browser without specifying in url) 
 (use `this` in place of websocket ip to automatically get machine's external ip - useful if chatserver is hosted on the same machine)

stop any of the scripts with `ctrl+c` (KeyboardInterrupt) or `ctrl+d`/`ctrl+z+Enter` (EOFError)
