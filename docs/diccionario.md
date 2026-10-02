# Diccionario de Datos (Borrador Inicial)

Este es el esquema inicial de los datos basado en la exploración de la muestra. Se irá actualizando cuando conectemos con la API real.

| Columna | Tipo de Dato (Python) | Descripción | Ejemplo |
|---------|------------------------|-------------|---------|
| Codigo  | String (Texto)         | Identificador único de la orden de compra. | 1234-5-LE26 |
| Nombre  | String (Texto)         | Título o descripción breve de la compra. | Computadores |
| Estado  | String (Texto)         | Situación actual de la orden (Aceptada, Enviada, Cancelada). | Aceptada |
| Monto   | Integer (Número)       | Valor total de la orden de compra en pesos chilenos (CLP). | 1500000 |