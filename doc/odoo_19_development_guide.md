# Módulo de Comisiones de Venta — Guía de la clase

**Crea un módulo desde cero en Odoo 19 con Agentes IA** Canal:
[@jcmontoya](https://youtube.com/@jcmontoya) | campuscleverit.es

---

# 🔴 ORDEN DE TRABAJO (SÍGUELO TAL CUAL)

Si sigues estos pasos en orden, terminas con el módulo funcionando.

1. Preparar entorno
2. Entender qué vamos a construir
3. Crear estructura del módulo con IA
4. Generar el código con IA
5. Refactorizar lo que la IA genera de más
6. Integrar el código en tu proyecto
7. Instalar el módulo
8. Resolver errores de instalación
9. Entender el código clave
10. Validar el resultado final

> Esta guía está pensada para seguir la clase paso a paso. No es documentación suelta.
> Está ordenada para que construyas la app completa sin perderte.

---

## 1. Antes de empezar

### Entorno de desarrollo

Necesitas una instalación de Odoo 19 funcionando en local.

- **Linux (recomendado):** usa tu entorno habitual
- **Windows/Mac con Docker:** también vale sin problema

> Si no tienes entorno listo, a continuación te dejo opciones:

- [Instalación con Docker](https://youtu.be/cshOU_Zp3bE?si=fjgkjlN1V0hm8r80)
- [Instalación en Mac](https://youtube.com/playlist?list=PLZ4jpQqTamn2Mme-0w43Kvin5Q4AWcQk3&si=__2jHsR0YcpEGWCD)
- [Instalación en Linux](https://campuscleverit.es/blog/odooexperto-1/como-instalar-odoo-19-en-linux-ubuntu-24-04-5)

### Versión de Odoo

**Odoo 19 Enterprise** pero el módulo funciona igual en **Community**.

### Editor

Usaré **Zed Editor** con GitHub Copilot. Puedes usar **PyCharm**, **VSCode**, **Cursor**
o cualquier editor con IA. El proceso es el mismo.

Entorno Odoo con ZED:
[Zed Editor](https://youtube.com/playlist?list=PLZ4jpQqTamn1jwYUUZCuJj4uOfNF6Q2Dx&si=k9GnDZgMDulMjUEt)

VS Code para Odoo:
[VSCode para Odoo](https://youtube.com/playlist?list=PLZ4jpQqTamn1NhcRT8e5Bzwe2OEQMO8uG&si=sepYo3bT0rp_RYwb)

### Repositorio

Todo el código de esta clase está disponible en:

[Repositorio GitHub](https://github.com/odooerpdevelopers/odoo19examples)

✔ Antes de seguir deberías tener:

- Odoo 19 arrancando
- acceso a tu carpeta `extra-addons` o la que uses para desarrollo
- un editor abierto
- acceso al repositorio y esta guía

---

## 2. Qué vamos a construir

Vamos a crear una app que calcula automáticamente las comisiones de los comerciales de
venta. Para simplificar, el cálculo será aplicar un porcentaje fijo sobre el total del
pedido, pero con la flexibilidad de configurar ese porcentaje por vendedor.

### Lo que nos pide el cliente:

> "Necesitamos un módulo para gestionar las comisiones de nuestros vendedores. Queremos
> poder configurar un porcentaje de comisión para cada vendedor, que se aplique
> automáticamente a los pedidos de venta. Además, necesitamos llevar un histórico de las
> comisiones generadas por cada pedido y poder consultarlas fácilmente desde el menú de
> ventas."

### Especificaciones técnicas

El módulo tendrá:

- **3 modelos**
- **herencia sobre `sale.order`**
- **menú propio dentro de Ventas**
- **vista de reglas**
- **vista de histórico de comisiones**
- **pestaña Comisión en el pedido de venta**

### Resultado final esperado

Al final del ejercicio deberías tener esto:

- Menú **Comisiones** dentro del módulo Ventas
- **Reglas de comisión** para configurar el % por vendedor
- **Pestaña Comisión** dentro de cada pedido de venta
- **Cálculo automático** del importe de comisión
- **Líneas históricas** que se generan al confirmar el pedido
- **Vista de comisiones generadas** con los datos clave

✔ Si al final no tienes todo esto funcionando, hay algo que revisar.

---

## 3. Crear la estructura del módulo con IA

### Objetivo de este paso

Primero no vamos a pedir código. Solo la estructura base del módulo.

### Prompt 1 — Crear la estructura del módulo

```text
Crea la estructura de carpetas y archivos vacíos para un módulo Odoo 19
llamado tl_sale_commission en la raíz del proyecto.

La estructura debe ser:
tl_sale_commission/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── sale_commission_rule.py
│   ├── sale_commission_line.py
│   └── sale_order.py
├── views/
│   ├── sale_commission_rule_views.xml
│   └── sale_order_views.xml
├── security/
│   └── ir.model.access.csv
└── static/
    └── description/

Solo crea los archivos vacíos, no escribas código todavía.
```

### Estructura esperada

```text
tl_sale_commission/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── sale_commission_rule.py
│   ├── sale_commission_line.py
│   └── sale_order.py
├── views/
│   ├── sale_commission_rule_views.xml
│   └── sale_order_views.xml
├── security/
│   └── ir.model.access.csv
└── static/
    └── description/

```

✔ Validación:

- La carpeta `tl_sale_commission` existe
- Están todas las carpetas necesarias
- Están todos los archivos vacíos
- Todavía no has pegado código

---

## 4. Generar el código con IA

### Objetivo de este paso

Ahora sí, pedimos al agente que genere el primer borrador completo del módulo.

### Prompt 2 — Generar el código

```text
Ahora sí, genera el código para tl_sale_commission y colócalo dentro de cada fichero correspondiente en el módulo
Genera el código completo para un módulo Odoo 19 de comisiones de vendedor
con las siguientes especificaciones:

MODELOS:
1. sale.commission.rule — modelo propio con campos:
   - name (Char, required)
   - user_id (Many2one a res.users, required, solo usuarios internos)
   - commission_percent (Float, required, digits 5,2)
   - active (Boolean, default True)
   - commission_line_ids (One2many inverso)
   - Constraint Odoo 19: UNIQUE(user_id, active)

2. sale.commission.line — modelo propio con campos:
   - order_id (Many2one a sale.order, required, ondelete cascade)
   - rule_id (Many2one a sale.commission.rule, required)
   - user_id (related de rule_id.user_id, store=True)
   - commission_percent (related de rule_id.commission_percent, store=True)
   - amount_total (related de order_id.amount_total, store=True, Monetary)
   - commission_amount (Monetary, computed, store=True)
   - currency_id (related de order_id.currency_id, store=True)
   - state (Selection: draft/confirmed/paid, default draft)

3. Herencia sale.order con campos:
   - commission_rule_id (Many2one a sale.commission.rule, computed por user_id, store, readonly=False)
   - commission_percent (Float computed, store)
   - commission_amount (Monetary computed, store)
   - commission_line_ids (One2many)
   - Override action_confirm para generar sale.commission.line al confirmar

VISTAS:
- Lista y formulario para sale.commission.rule
- Lista para sale.commission.line con decoration por estado
- Herencia vista formulario sale.order: pestaña Comisión con notebook
- 1 Menú Commissions dentro de sale.sale_menu_root
- 2 Menús dentro de Commissions: Reglas y Comisiones generadas

SEGURIDAD:
- Acceso completo para group_sale_manager
- Solo lectura para group_sale_salesman

> Importante: Usa Ruff (Astral) para formato y lint del código: 88 caracteres por línea,
> Generar las vistas "tree" usando la etiqueta <list>
> Todo el código debe estar en Inglés, incluyendo nombres de campos, menús, modelos y vistas, anotaciones. Se traducirá después usando los ficheros .po de Odoo
> Al finalizar solo imprime por pantalla "Tarea terminada".
```

### Qué debería generarte la IA

- `__manifest__.py`
- `__init__.py`
- `models/__init__.py`
- modelo `sale.commission.rule`
- modelo `sale.commission.line`
- herencia de `sale.order`
- vistas XML
- CSV de permisos
- icono (pedirlo aparte)

⚠️ **Importante:** aquí la IA genera un borrador. No es el resultado final.

✔ Validación:

- Existen los 3 modelos
- Existe el manifest
- Existen las vistas
- Existe el CSV de seguridad
- El módulo ya tiene forma completa

---

## 5. Refactorizar lo que la IA genera de más

### Objetivo de este paso

Este bloque es importante porque enseña algo real: **la IA acelera, pero el sistema lo
pone el dev**.

No todo lo que genere el agente debe quedarse.

### Puedes simplificar o mejorar

- revisar y optimizar la carga de campos calculados ¿Son necesarios?.
- dominios que no aporten nada
- detalles demasiado avanzados para una primera versión
- lógica que no enseñe un concepto nuevo

✔ Resultado esperado:

- modelos más limpios
- menos ruido
- mismo resultado funcional
- mensaje claro: **no haces copy-paste ciego de la IA**

---

## 6. Integrar el código en tu proyecto

### Objetivo de este paso

Pegar el código generado y refactorizado en tu módulo local.

### Archivos mínimos que debes completar

```text
tl_sale_commission/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── sale_commission_rule.py
│   ├── sale_commission_line.py
│   └── sale_order.py
├── views/
│   ├── sale_commission_rule_views.xml
│   └── sale_order_views.xml
├── security/
│   └── ir.model.access.csv
└── static/
    └── description/
        └── icon.png
```

### Orden recomendado

1. Manifest
2. Init
3. Modelos Python
4. Seguridad
5. Vistas XML
6. Icono

> Este orden ayuda a no perderte cuando luego aparezcan errores.

✔ Validación:

- Todos los archivos tienen contenido
- No hay imports rotos
- No falta ningún archivo que el manifest cargue

---

## 7. Instalar el módulo

### Pasos

- Reinicia Odoo
- Actualiza la lista de apps
- Busca `tl_sale_commission`
- Instala el módulo

### Qué debería pasar

- El módulo instala
- Aparece el menú **Comisiones** dentro de Ventas
- No hay traceback bloqueando la instalación

✔ Validación:

- instalación correcta
- módulo visible
- menús visibles

---

## 8. Resolver errores de instalación

### Importante

En este ejercicio los errores **no son un estorbo**, son parte del aprendizaje.

### Errores frecuentes al instalar

| Error                  | Causa                                          | Solución                                          |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------- |
| `Module not found`     | El módulo no está en el `addons_path`          | Añadir la carpeta al `addons_path` en `odoo.conf` |
| `field does not exist` | La vista referencia un campo no definido       | Revisar nombre del campo en Python y XML          |
| `ir.model.access`      | Falta el CSV o tiene error                     | Revisar formato del CSV y nombres de modelo       |
| `inherit_id not found` | El XML ID de la vista padre no existe          | Activar modo dev y revisar el External ID         |
| `Constraint violation` | Ya existe un registro que viola la restricción | La constraint está funcionando; corrige los datos |

### Qué debes hacer aquí

- leer el error completo
- ir a la línea o al archivo que falla
- corregir
- reiniciar si hace falta
- volver a instalar o actualizar

✔ Objetivo de este bloque: No esconder errores. Enseñar cómo se corrigen.

---

## 9. Entender el código clave

No hace falta explicar cada línea. Solo lo que enseña algo importante.

---

### 9.1 Modelo nuevo vs herencia

**Modelo nuevo** → crea tabla nueva en base de datos.

```python
class SaleCommissionRule(models.Model):
    _name = "sale.commission.rule"
    _description = "Regla de comisión"
```

**Herencia** → amplía un modelo ya existente.

```python
class SaleOrder(models.Model):
    _inherit = "sale.order"
```

✅ Idea clave:

- `_name` crea
- `_inherit` extiende

---

### 9.2 Tipos de campos usados

| Campo       | Cuándo aparece en este módulo    | Qué decir                 |
| ----------- | -------------------------------- | ------------------------- |
| `Char`      | `name`                           | texto corto               |
| `Float`     | `commission_percent`             | número decimal            |
| `Boolean`   | `active`                         | sí/no                     |
| `Many2one`  | `user_id`, `rule_id`, `order_id` | relación con otro modelo  |
| `One2many`  | `commission_line_ids`            | relación inversa, virtual |
| `Monetary`  | `commission_amount`              | importe con moneda        |
| `Selection` | `state`                          | lista cerrada de estados  |

📖 Documentación oficial Odoo:
[Fields](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#fields)

---

### 9.3 Relaciones entre modelos

#### Many2one

Una línea de comisión pertenece a una regla:

```python
rule_id = fields.Many2one(
    comodel_name="sale.commission.rule",
    string="Regla aplicada",
)
```

Esto sí existe en base de datos como clave foránea.

#### Ejemplo en SQL:

Tabla sale.commission.rule

| id  | name         | user_id | commission_percent | active |
| --- | ------------ | ------- | ------------------ | ------ |
| 1   | Regla Felipe | 5       | 10 %               | True   |
| 2   | Regla Ana    | 6       | 15 %               | True   |

---

Tabla res.users 

| id | name   | login        | active | share |
|----|--------|-------------|--------|-------|
| 5  | Felipe | felipe@mail | True   | False |
| 6  | Ana    | ana@mail    | True   | False |

#### One2many

Una regla tiene muchas líneas:

```python
commission_line_ids = fields.One2many(
    comodel_name="sale.commission.line",
    inverse_name="rule_id",
    string="Histórico de comisiones",
)
```

Esto es virtual. No existe como columna en base de datos.

✅ Idea clave: `One2many` y `Many2one` suelen ir en pareja.

#### Ejemplo en SQL:

Pedido (sale.order)

| id  | name  | user_id   | amount_total |
| --- | ----- | --------- | ------------ |
| 1   | SO001 | (5)Felipe | 125.00 €     |

---

Linea de comisión (sale.commission.line)

| id  | order_id | user_id   | product    | base_amount | commission_percent | commission_amount |
| --- | -------- | --------- | ---------- | ----------- | ------------------ | ----------------- |
| 1   | 1        | (5)Felipe | Producto A | 25.00 €     | 10 %               | 2.50 €            |
| 2   | 1        | (5)Felipe | Producto B | 100.00 €    | 10 %               | 10.00 €           |

📖 Documentación oficial Odoo:
[relational-fields](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#relational-fields)

---

### 9.4 Campo calculado importante del módulo

```python
commission_amount = fields.Monetary(
    string="Importe comisión",
    compute="_compute_commission_amount",
    store=True,
)
```

```python
@api.depends("order_id.amount_total", "commission_percent")
def _compute_commission_amount(self):
    for line in self:
        line.commission_amount = (
            line.order_id.amount_total
            * line.commission_percent
            / 100
        )
```

✅ Claves sobre los campos calculados.

- qué hace `@api.depends`
- qué cambia con `store=True`
- que puedes depender de campos anidados con notación punto

📖 Documentación oficial Odoo:
[Computed-fields](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#computed-fields)

---

### 9.5 models.Constraint — novedad Odoo 19

Antes se veía así:

```python
_sql_constraints = [
    ("unique_user", "UNIQUE(user_id)", "Ya existe una regla."),
]
```

En Odoo 19:

```python
# se implementa en la clase durante la clase en vivo
```

✅ Puedes ver al detalle coómo funciona models.Constraint y cómo crear índices
compuestos en esta guía:
[Migrando a Odoo 19](https://youtube.com/playlist?list=PLZ4jpQqTamn3iTbcZNT2XptPSj2L1i33-&si=DRVNVy8evYkXT4dj)

📖 Documentación oficial Odoo:
[Constraints-Indexes](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#constraints-and-indexes)

---

### 9.6 Override real: `action_confirm`

Aquí heredas un método de Odoo para añadir tu lógica cuando se confirma el pedido:

```python
def action_confirm(self):
    res = super().action_confirm()
    for order in self:
        if order.commission_rule_id:
            self.env["sale.commission.line"].create({
                "order_id": order.id,
                "rule_id": order.commission_rule_id.id,
                "state": "confirmed",
            })
    return res
```

✅ Ideas clave:

- `super()` llama a la lógica original de Odoo
- tú añades tu lógica después
- aquí nace el histórico de comisiones

---

### 9.7 El manifest — `__manifest__.py`

Es como el documento de identidad de un módulo.

```python
{
    "name": "Sale Commission",
    "version": "19.0.1.0.0",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_commission_rule_views.xml",
        "views/sale_order_views.xml",
    ],
}
```

---

### 9.8 Herencia XML — extender una vista

```xml
<record id="view_sale_order_form_commission" model="ir.ui.view">
  <field name="name">sale.order.form.commission</field>
  <field name="model">sale.order</field>
  <field name="inherit_id" ref="sale.view_order_form" />
  <field name="arch" type="xml">
    <notebook position="inside">
      <page string="Comisión" name="commission">
        <!-- contenido -->
      </page>
    </notebook>
  </field>
</record>
```

---

### 9.9 Seguridad — `ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_rule_manager,rule manager,model_sale_commission_rule,sales_team.group_sale_manager,1,1,1,1
access_rule_user,rule user,model_sale_commission_rule,sales_team.group_sale_salesman,1,0,0,0
```

✅ Idea clave: Sin permisos, el módulo puede instalar pero nadie podrá trabajar con él
correctamente. Está invisible para los usuarios.

📖 Documentación oficial Odoo — Security:
[Security](https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html)

---

### 9.10 Flujo mental para entender Odoo

```text
Menú → Acción → Modelo → Vista
```

1. El usuario hace clic en un menú
2. El menú dispara una acción
3. La acción carga un modelo y una vista
4. Odoo muestra los datos

Ejemplo:

```xml
<record id="action_sale_commission_rule" model="ir.actions.act_window">
    <field name="name">Reglas de comisión</field>
    <field name="res_model">sale.commission.rule</field>
    <field name="view_mode">list,form</field>
</record>

<menuitem
    id="menu_sale_commission_rules"
    name="Reglas"
    parent="menu_sale_commission_root"
    action="action_sale_commission_rule"/>
```

✅ Esto ayuda a entender el flujo de ejecución en Odoo y cómo se conectan los menús con
los modelos y las vistas.

---

## 10. Validación final

### Prueba funcional mínima

Haz esto en orden:

1. Crear una **regla de comisión** para un vendedor
2. Crear un **pedido de venta** con ese vendedor
3. Revisar la pestaña **Comisión**
4. Confirmar el pedido
5. Verificar que se ha creado la **línea de comisión**
6. Entrar en **Comisiones generadas**
7. Verificar importe, porcentaje, vendedor y estado

### Resultado esperado

Al final deberías ver:

- regla aplicada en el pedido
- porcentaje correcto
- importe de comisión calculado
- línea histórica generada
- menú y vistas funcionando

✔ Si esto pasa, el módulo está bien.

---

## Referencias oficiales

| Tema                     | Enlace                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| ORM — Fields completo    | [Fields](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#fields)                                   |
| Relational Fields        | [Relational-fields](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#relational-fields)             |
| Computed Fields          | [Computed-fields](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#computed-fields)                 |
| Constraints              | [Constraints-and-Indexes](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#constraints-and-indexes) |
| Views — herencia XML     | [Views](https://www.odoo.com/documentation/19.0/developer/reference/backend/views.html)                                         |
| Security — access rights | [Security](https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html)                                   |
| Manifest                 | [Module](https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html)                                       |

---

**Guía generada para construir la app completa paso a paso**

**[www.campuscleverit.es](http://www.campuscleverit.es)** Formación avanzada en Odoo.
