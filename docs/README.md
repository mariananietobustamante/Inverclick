# Documentación de Historias de Usuario — Inverclick API

Índice de las historias de usuario implementadas en el backend FastAPI.

| HU | Archivo | Estado |
|----|---------|--------|
| Seguridad V2 (Sesión 4) | [hu-seguridad-v2.md](./hu-seguridad-v2.md) | Implementada |
| Validaciones de negocio — Usuario | [hu-validaciones-usuario.md](./hu-validaciones-usuario.md) | Implementada |
| Constructoras, propiedades, leads y ventas (HU03) | [hu03-constructoras-propiedades-ventas.md](./hu03-constructoras-propiedades-ventas.md) | Implementada |
| Auth híbrida Keycloak / SSO (HU04) | [hu04-auth-hibrida-keycloak.md](./hu04-auth-hibrida-keycloak.md) | Implementada |
| Guía de pruebas paso a paso | [guia-pruebas-paso-a-paso.md](./guia-pruebas-paso-a-paso.md) | Disponible |

## Documentación técnica general

Para configuración, instalación y guía rápida de uso, consulta también:

- [`README`](../README) — Arranque completo en otro dispositivo, módulos y Swagger
- [`.env.example`](../.env.example) — Variables locales (JWT + Keycloak)
- [`requirements.txt`](../requirements.txt) — Dependencias Python

## Orden recomendado para probar

1. Sigue el arranque del [`README`](../README) (pasos 1 a 9) y la [guía de preparación](./guia-pruebas-paso-a-paso.md) (pasos 0.1 a 0.7)
2. Prueba las [validaciones de usuario](./hu-validaciones-usuario.md#paso-a-paso-por-función) — no requieren token en creación
3. Prueba la [seguridad JWT y autorización](./hu-seguridad-v2.md#paso-a-paso-por-función) — requieren token
4. Prueba [HU03 constructoras, propiedades, leads y ventas](./hu03-constructoras-propiedades-ventas.md)
5. (Opcional) Prueba [SSO Keycloak](./hu04-auth-hibrida-keycloak.md#paso-a-paso-para-probar)
