Actúa como un desarrollador senior de Odoo (versiones 18/19) trabajando como un agente
autónomo.

# 🎯 Objetivo

Crear un módulo completo de Odoo que resuelva la necesidad de negocio descrita a
continuación.

Debes entregar una solución funcional completa (no solo explicación), incluyendo
estructura del módulo, lógica, vistas y seguridad.

No te detengas en el análisis: implementa el resultado final.

# ⚙️ Reglas de versión Odoo

- Usar Odoo 18/19
- Las vistas tipo lista deben usar <list> (no <tree>)
- No usar attrs en XML
- Seguir buenas prácticas modernas de Odoo

# 🧠 Necesidad del negocio

El cliente quiere gestionar las comisiones de sus vendedores.

Necesita un sistema sencillo donde:

- Cada vendedor tenga un porcentaje de comisión
- Ese porcentaje se aplique automáticamente a sus pedidos de venta
- La comisión se calcule en base al total del pedido

Además, necesita:

- Ver la comisión directamente dentro de cada pedido de venta
- Tener una vista global con todas las comisiones generadas
- Mantener un histórico de comisiones

# ⚙️ Comportamiento esperado

- La comisión debe calcularse automáticamente
- Si cambia el vendedor o el total del pedido, la comisión debe actualizarse sola
- El usuario no debe poder modificar manualmente la comisión calculada
- Al confirmar un pedido de venta:
  - La comisión debe quedar registrada como histórico
- Las comisiones deben tener un estado (por ejemplo: borrador, confirmada, pagada)

# ⚠️ Consideración importante

- En esta primera versión, el sistema puede ser sencillo
- Pero debe estar preparado para evolucionar en el futuro (por ejemplo: comisiones más
  complejas, diferentes condiciones, etc.)

No sobrecomplicar la solución, pero tampoco limitar su crecimiento futuro.

# 🔐 Accesos

- Un vendedor debe poder ver sus comisiones
- Un responsable de ventas debe poder ver todas
- Solo usuarios con permisos adecuados pueden modificar configuraciones

# 🧾 Calidad del código

- Código limpio y organizado
- Archivos correctamente estructurados
- Vistas bien definidas y coherentes
- El módulo debe poder instalarse sin errores

# ⚡ Forma de trabajar

- Actúa de forma autónoma
- No pidas confirmaciones innecesarias
- Toma decisiones razonables si algo no está completamente definido
- Entrega una solución completa, no parcial

# ✅ Resultado esperado

- Generar todo el módulo completo con sus archivos
- Código listo para instalar en Odoo
- No dejar tareas pendientes

Al finalizar, imprime: Tarea terminada
