# Llevando mi skill de Linux del 63% al 80%

Plan de mejora progresiva para subir mi nivel en Linux, enfocado en administración de sistemas, automatización y diagnóstico, con aplicaciones directas al rol de DevOps/infra.

## Cronograma

### Bloque 1: Administración y Shell avanzado (2 semanas)
- Manejo de procesos, señales, prioridades (`top`, `nice`, `kill`, `at`, `cron`)
- Redirección avanzada, `xargs`, `find`, `grep`, `awk`, `sed`
- Variables de entorno y scripting en bash (con loops, funciones y condiciones)
- Manejo de logs (`journalctl`, `logrotate`, `rsyslog`)
- Usuarios, grupos, permisos ACL y `sudoers`

Meta: crear 3 scripts útiles reales para mi entorno (monitoreo, backup, hardening)

### Bloque 2: Seguridad práctica (2 semanas)
- `ufw`, `iptables`/`nftables` básicos
- Instalar y tunear `fail2ban`
- Manejo de claves SSH, permisos `.ssh`, agente, `ssh-copy-id`
- Chroot, jail básica, separación de procesos
- Hardening básico (disable servicios, suid, updates, `/etc/security`)

Meta: endurecer mi propia EC2 o VPS productiva y documentar los pasos

### Bloque 3: Servicios en producción (3 semanas)
- Manejo de systemd (servicios personalizados, targets, units)
- Configuración avanzada de Nginx (reverse proxy, upstream, TLS, headers)
- Supervisión de procesos con `supervisord` o `systemd`
- Tareas automáticas con `cron`, `anacron`, `systemd timers`

Meta: tener mi stack Django + Nginx + Docker con logs y reinicios controlados vía systemd

### Bloque 4: Diagnóstico y performance (2 semanas)
- Herramientas: `htop`, `iotop`, `dstat`, `lsof`, `strace`, `tcpdump`, `netstat`, `ss`
- Monitoreo de servicios con `monit`, `psutils`, o integración con Grafana/Prometheus
- Diagnóstico de red (MTU, ping, traceroute, DNS, logs del kernel)

Meta: resolver 3 escenarios simulados de problemas (red lenta, disco lleno, proceso zombie)
