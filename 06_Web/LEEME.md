# Web local · PRETEXTUDA

Requiere Python 3.10+. Ejecutar `python server.py` dentro de esta carpeta (Windows: `py server.py`). Abrir en tu navegador local la dirección de loopback con puerto 8000. Ctrl+C detiene el servidor.

Funciona: página adaptable, formulario de consulta, validación, consentimiento promocional opcional y contactos SQLite locales. No envía correos ni procesa pagos. El archivo config.json es público: nunca guardar secretos allí. Los enlaces HTTPS de agenda, redes, comunidad y checkout se configuran con datos reales y se reinicia el servidor.

Ofertas recibidas: workshop de 2 horas, $27; lectura individual con informe, $70. Ambos importes tienen USD confirmado. Colombia, zona America/Bogota. El cuaderno está incluido en la oferta, no es un regalo de captación. La ruta interna /guia.pdf permite revisar el material localmente, no constituye un sistema de acceso pagado.

Administrar localmente: `python contactos.py export --marketing-only --output suscripciones.csv`; eliminar un registro: `python contactos.py delete --email persona@example.com`. Nunca incluir la carpeta datos en publicaciones o compartir sus exportaciones.

Para producción: definir política de tratamiento de datos Colombia y condiciones de venta; elegir hosting HTTPS, email autenticado con baja real, agenda y proveedor de pago compatible con COP/USD y país. Wompi, PayU o Mercado Pago son candidatos para evaluar, no cuentas configuradas. No asumir Stripe disponible para una entidad colombiana.

Usar checkout externo y validar confirmación real; si se automatiza, verificar webhooks firmados y evitar duplicados. Entregar el cuaderno a participantes tras compra confirmada mediante proveedor o flujo privado. El servidor local no implementa esa autorización ni debe exponerse a Internet. No capturar tarjetas aquí. Probar compra/cancelación/confirmación/baja antes del lanzamiento público.

Actualizar los textos de privacidad, contacto y condiciones con datos de Aisse antes de captar contactos reales. La base local mantiene la última elección de marketing, no un historial completo de consentimiento.
