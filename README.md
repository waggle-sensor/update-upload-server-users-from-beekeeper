# Update Upload Server Users from Beekeeper

This is script updates an [upload server's](https://github.com/waggle-sensor/beehive-upload-server) users based on nodes in a [Beekeeper](https://github.com/waggle-sensor/beekeeper). It is primarily intended to be run as a cronjob.

This script expects the following env vars as configuration:

* `BEEKEEPER_STATE_ENDPOINT`: Endpoint for Beekeeper state API.
* `BEEHIVE_NAME`:  Name of Beehive.
* `UPLOAD_SERVER_HOST`: Beehive's upload server host.
* `UPLOAD_SERVER_PORT`: Beehive's upload server port.
* `UPLOAD_SERVER_USER`: Beehive's upload server user.
* `UPLOAD_SERVER_KEY`: Path to Beehive's upload server key.

Additionally, an ssh key pair must be mounted at `UPLOAD_SERVER_KEY` for authentication with the upload server.
