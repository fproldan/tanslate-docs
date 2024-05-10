# Unidad de manipulación

Una unidad de manipulación es una abstracción para rastrear cantidades de artículos que se mueven o almacenan juntos. No reemplaza los números de lote o de serie, la fabricación de un artículo ni la funcionalidad del paquete de productos, pero puede complementarlos como una forma de obtener información de manera conveniente que, de otro modo, requeriría muchas pulsaciones de teclas para ingresar.

Al asignar una identificación única a la unidad de manipulación, es posible capturar mediante un escáner el artículo, la cantidad neta, la unidad de medida y la marca de tiempo de la transacción anterior, y luego actuar sobre esa información en contexto, de acuerdo con la [matriz de decisión]( ./matriz.md). Beam agrega un nuevo tipo de documento, Unidad de manipulación, para implementar esta funcionalidad en ERPNext.

![Captura de pantalla de la vista de lista del tipo de documento de la Unidad de manipulación. La lista muestra varias unidades de embalaje nuevas que se crearon para artículos recibidos mediante un recibo de compra.](./assets/handling_unit_list.png)

## Vistas de lista
Generalmente, escanear una Unidad de Manejo en una vista de lista se filtrará para mostrar todas las transacciones del tipo de documento con la Unidad de Manejo apropiada.

## Recibo de compra
Para los recibos de compra, las unidades de embalaje se generan y el usuario no puede suministrarlas.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 40 unidades |


## Factura de compra
Para las facturas de compra con "Actualizar stock" marcado, las unidades de embalaje se generan y el usuario no puede suministrarlas.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 40 unidades |

Cuando "Actualizar stock" _no_ está marcado, se pueden escanear para facilitar la entrada de datos, pero no tiene ningún efecto en el Libro mayor de stock.

## Nota de entrega
Para el Albarán de entrega, se consumen Unidades de embalaje. En el caso de que se entregue menos de la cantidad total asociada con la Unidad de Manejo, la Unidad de Manejo existente se referirá a la cantidad restante (neta).

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 20 unidades |

Libro mayor de existencias o transacción posterior
| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 20 unidades |


## Factura de venta
Para una factura de venta donde está marcado "Actualizar stock", se consumen unidades de embalaje. En el caso de que se entregue menos de la cantidad total asociada con la Unidad de Manejo, la Unidad de Manejo existente se referirá a la cantidad restante (neta).

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 15 unidades |

Libro mayor de existencias o transacción posterior
| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 5 unidades |

Cuando "Actualizar stock" _no_ está marcado, se pueden escanear para facilitar la entrada de datos, pero no tiene ningún efecto en el Libro mayor de stock.

La siguiente captura de pantalla muestra el libro de contabilidad de existencias del artículo Cloudberry. La primera fila muestra la recepción de 60 libras de la fruta mediante un Recibo de Compra, y la segunda fila es después de la venta de 25 libras mediante una Factura de Venta que tenía 'stock actualizado'. Tenga en cuenta que ambas transacciones hacen referencia a la misma Unidad de Manejo.

![Captura de pantalla del libro de contabilidad de existencias que rastrea el recibo y las ventas del artículo Cloudberry.](./assets/stock_ledger_after_sale.png)

## Entrada de acciones

### Envío a Contratista, Transferencia de Material para Fabricación y Transferencia de Material
Cuando el material se transfiere de un almacén a otro, se generará una nueva Unidad de Manipulación, incluso si se está transfiriendo toda la Unidad de Manipulación. En el caso de que se mueva menos de la cantidad total asociada con una unidad de embalaje de un almacén a otro, se genera una nueva unidad de embalaje para las nuevas unidades. Los escaneos o búsquedas posteriores de la unidad de manipulación original (123) devolverán el resto o la cantidad neta.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ----------------------- | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | -40 unidades |
| ciruela de coco | Almacén de subcontratistas | 456 | 40 unidades |

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | -20 unidades |
| ciruela de coco | Trabajo en progreso | 456 | 20 unidades |


Al cancelar una entrada de stock, el usuario tendrá la opción de volver a combinar o dejar que las unidades de manipulación sigan siendo rastreadas por separado.

![Captura de pantalla del diálogo de recombinación](./assets/recombine.png)

### Reempaquetado y fabricación

En el caso de un Reempaque, Salida de Material o Consumo de Material para Fabricación, se genera una nueva Unidad de Manejo para las nuevas cantidades.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | -40 unidades |
| ciruela de coco | Trastero | 789 | 1 Caja de 40 |


En el caso de que se consuma menos de la cantidad total asociada con una Unidad de Manejo, los escaneos o búsquedas posteriores de la Unidad de Manejo (123) original devolverán el resto o la cantidad neta.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | -20 unidades |
| Puré de cocociruela | Trabajo en progreso | 012 | 1 litro |
| ciruela de coco | Chatarra | | 1 unidad |

#### Artículo de desecho de lista de materiales
En una entrada de stock de fabricación o reempaquetado, los artículos de desecho se pueden alternar para crear una unidad de manipulación correspondiente a su cantidad de desecho. Esto se puede cambiar después de enviar una lista de materiales.

![Captura de pantalla de elementos de desecho de la lista de materiales que muestra la configuración](./assets/bom_scrap_item.png)

### Problema de material, consumo de material para fabricación

En ambos casos no existe ningún movimiento compensatorio ni creación de partidas.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | -20 unidades |


| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trabajo en progreso | 123 | -20 unidades |

### Recibo de material
En el caso de Recepción de Material, se genera una nueva Unidad de Manejo para cada artículo.

| Artículo | Almacén | Unidad de manipulación | Cantidad |
| ---------------- | ------------------ | -------------- | --------------:|
| ciruela de coco | Trastero | 123 | 20 unidades |