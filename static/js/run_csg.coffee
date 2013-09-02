$ ->
  attributes = {
    code: 'se.liu.screencast.twsclient.Main'
    archive: "#{window.static_url}applet/twSClient.jar"
    width: 1000
    height: 700
  }
  parameters = {
    # There's a reference in the jnlp to applet/twSClient.jar,
    # which might not go to the correct place considering the
    # static things. Might want to generate it in django
    # to resolve that.
    jnlp_href: "#{window.static_url}screencast_webstart.jnlp"
  }
  $('#launch_app').click ->
    deployJava.runApplet(attributes, parameters, '1.7.0')
