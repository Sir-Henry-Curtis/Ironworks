<?php

define("HOST", "192.168.1.6"); // The host you want to connect to.
define("USER", "desktop"); // The database username.
define("PASSWORD", "aic9i1tdpw"); // The database password.
define("DATABASE", "desktop"); // The database name.

$mysqli = new mysqli(HOST, USER, PASSWORD, DATABASE);
// If you are connecting via TCP/IP rather than a UNIX socket remember to add the port number as a parameter.