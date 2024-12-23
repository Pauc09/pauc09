# Conversor de Monedas

## Descripción
Este proyecto es un conversor de monedas desarrollado en Java que utiliza la API "ExchangeRate-API" para obtener tasas de cambio actualizadas. Permite convertir cantidades entre monedas, mostrar tasas de cambio disponibles y cambiar la moneda base de manera interactiva.

---

## Requisitos

- **Librería Gson:** [Descargar](https://github.com/google/gson).
- **Conexión a Internet:** Necesaria para las solicitudes a la API.
- **Clave de API:** Regístrate en [ExchangeRate-API](https://www.exchangerate-api.com/) para obtener una clave.

---

## Configuración
1. Sustituye `YOUR_API_KEY` en la clase `API` con tu clave:

```java
private static final String API_KEY = "YOUR_API_KEY";

