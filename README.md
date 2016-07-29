[fork form marathon-autoscale repo from the mesosphere company]

Simple app for generating rsyslog forward config based on marathon app label


Caveats of v0:
  -since we have no way of knowing if an event is creating/updating/deleting an
  app, we replace the app list everytime an api_post_event comes.
