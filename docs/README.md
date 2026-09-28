# Documentación de Historias de Usuario — Inverclick API

Índice de las historias de usuario implementadas en el backend FastAPI.

| HU | Archivo | Estado |
|----|---------|--------|
| Seguridad V2 (Sesión 4) | [hu-seguridad-v2.md](./hu-seguridad-v2.md) | Implementada |
| Validaciones de negocio — Usuario | [hu-validaciones-usuario.md](./hu-validaciones-usuario.md) | Implementada |
| Auth híbrida Keycloak / SSO (HU04) | [hu04-auth-hibrida-keycloak.md](./hu04-auth-hibrida-keycloak.md) | Implementada |
| Guía de pruebas paso a paso | [guia-pruebas-paso-a-paso.md](./guia-pruebas-paso-a-paso.md) | Disponible |

## Documentación técnica general

Para configuración, instalación y guía rápida de uso, consulta también:

- [`README`](../README) — Guía de desarrollo, módulos y pruebas en Swagger
- [`.env.example`](../.env.example) — Variables locales (JWT + Keycloak)

## Orden recomendado para probar

1. Lee la [guía de preparación](./guia-pruebas-paso-a-paso.md) (pasos 0.1 a 0.7)
2. Prueba las [validaciones de usuario](./hu-validaciones-usuario.md#paso-a-paso-por-función) — no requieren token en creación
3. Prueba la [seguridad JWT y autorización](./hu-seguridad-v2.md#paso-a-paso-por-función) — requieren token
4. Prueba módulos de negocio en Swagger: **Construction Companies**, Real Estate, Sales, Banks, Leads
5. (Opcional) Prueba [SSO Keycloak](./hu04-auth-hibrida-keycloak.md#paso-a-paso-para-probar)
