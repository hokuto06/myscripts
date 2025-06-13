# myscripts 🚀
## Esta es una colección de algunos de los scripts que utilizaba en mi último rol como administrador de redes on-prem . 


Docker Compose stack que levanta **todos mis sitios en producción**  
(Python + Nginx + Docker, sin vendor-lock y fácil de clonar).

| Servicio | Tech | Rol | Carpeta |
|----------|------|-----|---------|
| **excel** | Nginx 1.27 | Reverse-proxy HTTPS + servir estáticos | [`/excel`](nginx) |
| **ruckus** | Django 4 + DRF | Backend /admin + REST para el blog | [`/ruckus`](django-api) |
| **switches** | python | scrips para setear switches | [`/switches`](django_blog_front) |
| **excel** | python | scripts para procesar planillas | [`/excel`](app) |

> **Nota**: la antigua carpeta `php/` quedó fuera del repositorio (solo vive en mi server).

---