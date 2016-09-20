## CHANGELOG

### v0.0.6

- Making config file optional. If the user specifies mandatory attrs i.e.

  ```
  host
  port
  user
  password
  ```

  there isn't a point in cribbing about the lack of a configfile. If both command line params and config file provided - command line params override config file.
