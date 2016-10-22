exec {
  command = "/usr/bin/telegraf -config-directory=/etc/telegraf/telegraf.d"
  splay = "5s"
  reload_signal = "SIGHUP"
  kill_timeout = "30s"
}

template {
  source = "/etc/telegraf/telegraf.conf.ctmpl"
  destination = "/etc/telegraf/telegraf.conf"
}

log_level = "ERR"
